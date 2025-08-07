from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .compiler import Compiler 

def code_editor(req):
    return render(req,"editor.html",{})

 

class CompileView(APIView):
    
    def post(self, request):
        code = request.data.get("code")
        input_data = request.data.get("input")
        lang = request.data.get("lang")

        if not code or not lang:
            return Response({"error": "Missing code or language."}, status=status.HTTP_400_BAD_REQUEST)
        
        compiler = Compiler()
        try:
            if lang == "Cpp":
                result = compiler.compile_cpp(code)
            elif lang == "Java":
                result = compiler.compile_java(code)
            elif lang == "Python":
                result = compiler.compile_python(code)
            else:
                return Response({"error": "Unsupported language."}, status=status.HTTP_400_BAD_REQUEST)

            return Response(result)
        except Exception:
            return Response({"error": "An error occurred while processing."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
