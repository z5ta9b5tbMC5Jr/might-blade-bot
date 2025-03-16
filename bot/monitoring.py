from prometheus_client import start_http_server, Summary, Counter, Histogram
import time

REQUEST_TIME = Summary('request_processing_seconds', 'Tempo de processamento das requisições')
COMMAND_COUNTER = Counter('bot_commands', 'Contador de comandos executados', ['command'])

def monitor_requests(command_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            COMMAND_COUNTER.labels(command=command_name).inc()
            
            try:
                result = func(*args, **kwargs)
                request_time = time.time() - start_time
                REQUEST_TIME.observe(request_time)
                return result
            except Exception as e:
                raise e
        return wrapper
    return decorator 