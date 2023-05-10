from sqlite3 import Timestamp
from unicodedata import category, name
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
from .models import *
from .forms import *
import datetime
import random
import string


def home(request):


    return render(request, 'home\index.html',{
        'product': "gf",

    })
