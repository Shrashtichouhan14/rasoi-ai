import os
import json
import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

genai.configure(api_key=settings.GEMINI_API_KEY)

def index(request):
    # This passes the session data directly to the HTML when the page loads
    context = {
        'initial_ingredients': request.session.get('ingredients', [])
    }
    return render(request, 'index.html', context)

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # 1. Initialize Memory
            if 'ingredients' not in request.session:
                request.session['ingredients'] = []
            if 'constraints' not in request.session:
                request.session['constraints'] = []
            if 'last_bot_response' not in request.session:
                request.session['last_bot_response'] = "" # <--- MEMORY FIX
            
            current_ingredients = request.session['ingredients']
            current_constraints = request.session['constraints']
            last_bot_msg = request.session['last_bot_response']

            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # --- CONTEXT-AWARE PROMPT ---
            system_instruction = f"""
            You are an expert Chef Consultant.
            
            Current Pantry: {", ".join(current_ingredients)}
            Current Constraints: {", ".join(current_constraints)}
            
            CONTEXT (What you said last time): "{last_bot_msg}"
            User's New Input: "{user_message}"
            
            YOUR GOAL: meaningful conversation. Stop looping.

            STRICT LOGIC STEPS:

            1. **CHECK FOR SELECTION (CRITICAL)**:
               - Look at the "CONTEXT". Did you just offer numbered options (1, 2, 3)?
               - If YES, and User's Input is "3", "the third one", "yes", or the name of the dish:
                 - **STOP SUGGESTING.**
                 - **GO TO STEP 5 (RECIPE).**

            2. **INTENT DETECTION**:
               - **Clearing:** "reset", "clear", "tasty", "thanks" -> Set action="clear_data".
               - **Gathering:** If user lists new items ("I have oil") -> Add to pantry.
               - **Suggesting:** If user asks "what can I cook" -> Go to Step 3.
            
            3. **FLAVOR INTERVENTION (The Missing Link)**:
               - Look at the pantry. Is it possible to make BOTH Sweet AND Savory dishes? 
                 (e.g. Rice + Milk can be Pudding OR Fried Rice. Bread + Egg can be French Toast OR Omelette).
               - **IF YES** AND user has NOT specified "sweet" or "spicy":
                 - **STOP.** Do not suggest dishes yet.
                 - **ASK:** "I see we can go two ways. Would you prefer something **Sweet** (like [Dish A]) or **Spicy** (like [Dish B])?"
               - **IF NO** (Ingredients are clearly only savory, like Onion + Garlic):
                 - Proceed to Step 4.

            4. **SUGGESTION PHASE** (Only if user hasn't selected a dish yet):
               - Suggest 3 distinct options numbered 1, 2, 3.
               - Format: "Here are 3 ideas:<br><br>1. [Dish A]<br>[Short Description]<br><br>2. [Dish B]<br>[Short Description]<br><br>3. [Dish C]<br><br>[Short Description]<br>Which one sounds good?"

            5. **RECIPE GENERATION**:
               - Provide the recipe for the selected dish.
               - **FORMATTING RULES (Use HTML):**
                 - Put ingredients in a list.
                 - Number the steps clearly.

            RECIPE TEMPLATE:
            "🍽️ <b>[Dish Name]</b><br><br><b>Ingredients:</b><br>- [Item 1]<br>- [Item 2]<br><br><b>Instructions:</b><br>1. [Step 1]<br><br>2. [Step 2]<br><br>3. [Step 3]"

            Output strictly valid JSON:
            {{
                "action": "chat", 
                "new_ingredients_found": [], 
                "new_constraints_found": [],
                "items_to_remove": [], 
                "bot_response": "Response string here"
            }}
            """

            response = model.generate_content(system_instruction)
            
            # JSON Parsing
            text = response.text
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1:
                parsed_response = json.loads(text[start:end+1])
            else:
                parsed_response = {"action": "chat", "bot_response": "Could you say that again?"}

            # --- PYTHON LOGIC ---
            action = parsed_response.get('action', 'chat')
            bot_reply = parsed_response.get('bot_response', '')

            # SAVE CONTEXT FOR NEXT TURN
            request.session['last_bot_response'] = bot_reply 

            if action == 'clear_data':
                request.session.flush() # Clears everything
            else:
                # Update Ingredients
                raw_items = parsed_response.get('new_ingredients_found', [])
                new_items = [i.strip().title() for i in raw_items]
                if new_items:
                    updated_list = sorted(list(set(current_ingredients + new_items)))
                    request.session['ingredients'] = updated_list
                    request.session.modified = True 
                
                # Update Constraints
                new_constraints = parsed_response.get('new_constraints_found', [])
                if new_constraints:
                    updated_constraints = list(set(current_constraints + new_constraints))
                    request.session['constraints'] = updated_constraints
                    request.session.modified = True
                
                # Remove Items
                items_to_remove = parsed_response.get('items_to_remove', [])
                if items_to_remove:
                    current = request.session['ingredients']
                    cleaned = [i for i in current if i.lower() not in [x.lower() for x in items_to_remove]]
                    request.session['ingredients'] = cleaned
                    request.session.modified = True

            return JsonResponse({
                'response': bot_reply,
                'current_ingredients': request.session.get('ingredients', [])
            })

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def clear_session(request):
    request.session.flush()
    return JsonResponse({'status': 'cleared'})