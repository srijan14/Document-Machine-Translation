export IP="0.0.0.0"
export PORT=5000
export URL_ROOT="/translator"
export CONFIG="./available_models/conf.json"

# NOTE that these parameters are optionnal
# here, we explicitely set to default values
python server.py --ip $IP --port $PORT --url_root $URL_ROOT --config $CONFIG
