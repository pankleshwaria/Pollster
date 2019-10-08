from django.shortcuts import render


# Display the home page
def index(request):
    return render(request, 'pages/index.html')

