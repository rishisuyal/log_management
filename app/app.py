from flask import Flask, Response, jsonify, request
from kafka import KafkaConsumer as cons
from celery_app import  produce_to_kafka

app = Flask(__name__,template_folder='templates')
app.config['login_count'] = 0
app.config['topic'] = 'topic-1'
topic = app.config['topic']

app.config['login_count'] = app.config['login_count'] + 1

def create_consumer():
    return cons('topic-1', bootstrap_servers=['kafka:9092'], enable_auto_commit=True)

@app.route('/start')
def start():

    return Response(stream_template('home.html',data=consume_messages()))

def consume_messages():
    consumer = create_consumer()
    for message in consumer:
        yield (str(message.value) + '\n').encode('utf-8')
def stream_template(template_name, **context):
    app.update_template_context(context)
    template = app.jinja_env.get_template(template_name)
    streaming = template.stream(context)
    return streaming

@app.route('/prod', methods=['POST'])
def produce():
    global celery_id
    status = request.json.get('status', False)

    if status:
        async_result = produce_to_kafka.AsyncResult(str(celery_id))
        async_result.abort()
        print(celery_id)
        return jsonify({"message": "Producer stopping"})

    task = produce_to_kafka.delay()
    celery_id = task

    return jsonify({"message": "Producer started"})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
