{
  "displayName": "Customer Support Chatbot",
  "defaultLanguageCode": "en",
  "intents": [
    {
      "name": "projects/YOUR_PROJECT_ID/agent/intents/GREETING_INTENT_ID",
      "displayName": "Greeting Intent",
      "trainingPhrases": [
        {
          "parts": [
            {
              "text": "Hello"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "Hi"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "Hey there"
            }
          ]
        }
      ],
      "responses": [
        {
          "text": [
            "Hello! How can I assist you today?",
            "Hi there! What can I help you with?"
          ]
        }
      ],
      "outputContexts": [
        {
          "name": "projects/YOUR_PROJECT_ID/agent/sessions/session_id/contexts/greeting",
          "lifespanCount": 5
        }
      ]
    },
    {
      "name": "projects/YOUR_PROJECT_ID/agent/intents/FAQ_INTENT_ID",
      "displayName": "FAQ Intent",
      "trainingPhrases": [
        {
          "parts": [
            {
              "text": "What are your business hours?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "How can I contact support?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "What services do you offer?"
            }
          ]
        }
      ],
      "responses": [
        {
          "text": [
            "Our business hours are 9 AM to 5 PM, Monday to Friday.",
            "You can contact support via email at support@example.com."
          ]
        }
      ],
      "outputContexts": [
        {
          "name": "projects/YOUR_PROJECT_ID/agent/sessions/session_id/contexts/faq",
          "lifespanCount": 5
        }
      ]
    },
    {
      "name": "projects/YOUR_PROJECT_ID/agent/intents/SUPPORT_INTENT_ID",
      "displayName": "Support Intent",
      "trainingPhrases": [
        {
          "parts": [
            {
              "text": "I need help with my order"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "Can you assist me with a technical issue?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "I have a question about my account"
            }
          ]
        }
      ],
      "responses": [
        {
          "text": [
            "Sure! Please provide your order number or describe the issue.",
            "I'm here to help! What seems to be the problem?"
          ]
        }
      ],
      "parameters": [
        {
          "name": "order_number",
          "displayName": "Order Number",
          "entityType": "@sys.number",
          "mandatory": true,
          "prompts": [
            "Please provide your order number."
          ]
        }
      ]
    },
    {
      "name": "projects/YOUR_PROJECT_ID/agent/intents/ORDER_STATUS_INTENT_ID",
      "displayName": "Order Status Intent",
      "trainingPhrases": [
        {
          "parts": [
            {
              "text": "What is the status of my order?"
            }
          ]
        },
        {
          "parts": [
            {
              "text": "Can you check my order status?"
            }
          ]
        }
      ],
      "responses": [
        {
          "text": [
            "Please provide your order number to check the status."
          ]
        }
      ],
      "inputContextNames": [
        "projects/YOUR_PROJECT_ID/agent/sessions/session_id/contexts/support"
      ]
    }
  ],
  "entities": [
    {
      "name": "projects/YOUR_PROJECT_ID/agent/entities/ORDER_STATUS_ENTITY_ID",
      "displayName": "Order Status",
      "entries": [
        {
          "value": "shipped",
          "synonyms": ["sent", "dispatched"]
        },
        {
          "value": "pending",
          "synonyms": ["awaiting", "not yet sent"]
        }
      ]
    }
  ]
}
