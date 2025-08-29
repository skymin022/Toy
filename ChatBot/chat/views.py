from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
from llama_cpp import Llama


MODEL_PATH = "../models/llama-3-Korean-Bllossom-8B-Q4_K_M.gguf"
llm = Llama(model_path=MODEL_PATH, n_ctx=1024, n_gpu_layers=0)


def chat_page(request):
    return render(request, "chat/chat.html")


@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)

            print(f"Received message: {user_message}")

            start_time = time.time()

            generation_params = {
                "max_tokens": 150,
                "temperature": 0.7,
                "top_p": 0.9,
                "echo": False,
            }

            response = llm(user_message, **generation_params)
            answer = response['choices'][0]['text'].strip()

            elapsed = time.time() - start_time
            print(f"Response generated in {elapsed:.2f} seconds")

            # 예상 소요 시간 포함 응답
            return JsonResponse({
                "response": answer,
                "elapsed_seconds": round(elapsed, 2),
                "message": f"응답에 약 {round(elapsed, 2)}초 소요되었습니다."
            })
        except Exception as e:
            print(f"Error occurred: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "POST method required"}, status=405)
