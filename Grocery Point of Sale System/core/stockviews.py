from sqlite3 import Timestamp
from unicodedata import category, name
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
from .models import *
from .forms import *
from .decorators import *
import datetime
import random
import json


@allowed_users(allowed_roles=['admin', 'operator'])
def stocklist(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # add the dictionary during initialization
    context["dataset"] = Stock.objects.all()
         
    return render(request, "stock/index.html", context)


@allowed_users(allowed_roles=['admin', 'operator'])
def editstock(request):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # add the dictionary during initialization
    context["dataset"] = Stock.objects.all()
         
    return render(request, "stock/index.html", context)