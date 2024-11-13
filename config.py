k = int(2e20)  # size of the group Zp, any big value is okay
HOST = "0.0.0.0"
API_PORT = 8000
DEALER_PORT = 8080
LOCAL_HOST = "127.0.0.1"
URL_PREFIX = f"http://{LOCAL_HOST}:{API_PORT}"
DEALER_PREFIX = f"http://{LOCAL_HOST}:{DEALER_PORT}"
MODEL_FILE = "./model.joblib"
