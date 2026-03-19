import json
import os
from mistralai import Mistral

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        user_message = body.get('message', '')

        if not user_message:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No message provided'})
            }

        client = Mistral(api_key=os.environ['MISTRAL_API_KEY'])
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": user_message}]
        )

        reply = response.choices[0].message.content

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'reply': reply})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
        