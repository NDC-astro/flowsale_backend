import json
from datetime import datetime
from pymongo import MongoClient
from decouple import config
from django.utils.deprecation import MiddlewareMixin

class MongoLogMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        mongo_uri = config('MONGO_HOST')
        self.client = MongoClient(mongo_uri)
        self.db = self.client[config('MONGO_DB_NAME')]
        self.collection = self.db['user_logs']
        # Explicitly mark middleware as synchronous
        self.async_mode = False

    def process_request(self, request):
        request.mongo_log_data = {
            'timestamp': datetime.now(),
            'method': request.method,
            'path': request.path,
            'user': request.user.username if request.user.is_authenticated else 'Anonymous',
            'ip': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }

    def process_response(self, request, response):
        if hasattr(request, 'mongo_log_data'):
            log_data = request.mongo_log_data
            log_data.update({
                'status_code': response.status_code,
                'response_length': len(response.content) if hasattr(response, 'content') else 0,
            })

            if request.user.is_authenticated and request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                if '/api/clients/' in request.path or '/api/fournisseurs/' in request.path:
                    action_type = "Création" if request.method == 'POST' else \
                                "Modification" if request.method in ['PUT', 'PATCH'] else "Suppression"
                    entity = "Client" if '/clients/' in request.path else "Fournisseur"
                    log_data['action'] = f"{action_type} {entity}"
                    log_data['details'] = {
                        'url': request.path,
                        'body': getattr(request, '_body', b'').decode('utf-8') if hasattr(request, '_body') else None
                    }

            try:
                self.collection.insert_one(log_data)
            except Exception as e:
                print(f"[MongoLog Error] {e}")

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip