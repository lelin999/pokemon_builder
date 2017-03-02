from django.shortcuts import render
from django.http import JsonResponse
from ..login.models import User

# Create your views here.
def index(request):
    user = User.objects.get(id=request.session["id"])
    return render(request, '/teambuilder/index', {"user":user})

def stat_ajax(request):
    errors = []
    if request.method != 'POST':
        errors.append("Please use the form to calculate Pokemon data.")
    else:
        pokemon = {
            "id":request.POST["id"],
            "nature":request.POST["nature"],
            "hp_iv":request.POST["hp_iv"],
            "hp_ev":request.POST["hp_ev"],
            "atk_iv":request.POST["atk_iv"],
            "atk_ev":request.POST["atk_ev"],
            "def_iv":request.POST["def_iv"],
            "def_ev":request.POST["def_ev"],
            "spa_iv":request.POST["spa_iv"],
            "spa_ev":request.POST["spa_ev"],
            "spd_iv":request.POST["spd_iv"],
            "spd_ev":request.POST["spd_ev"],
            "spe_iv":request.POST["spe_iv"],
            "spe_ev":request.POST["spe_ev"],
        }
        if request.POST["id"] == "":
            errors.append("Please select a Pokemon!")
        if request.POST["nature"] == "":
            errors.append("Please select a nature!")
    if len(errors) == 0:
        return JsonResponse({"success":True, "pokemon":pokemon})
    else:
        return JsonResponse({"success":False, "errors":errors})

'''
route planning:
calculate(postData, create=False): sends POST async request to /calc/, route runs validate
    returns JSONResponse: valid = true w/ object, invalid = false w/ errors
    JQuery success - adds pokemon to belt

delete(roster_id): sends GET request to delete the pokemon

battle(player_id): Roster model objects compare each other, then returns winner, switching their leaderboard positions
    generates new leaderboard position for unranked players




'''
