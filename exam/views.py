from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Agentname, AnnouncedLgaResults, AnnouncedPuResults, AnnouncedStateResults, AnnouncedWardResults, AuthGroup, AuthGroupPermissions, AuthPermission, AuthUser, AuthUserGroups, AuthUserUserPermissions, DjangoAdminLog, DjangoContentType, DjangoMigrations, DjangoSession, Lga, Party, PollingUnit, States, Ward
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.generic import CreateView, FormView, ListView
from django.urls import reverse_lazy
from .forms import PollingUnitForm
from django.views import View

from django import forms
from .models import PollingUnit


class AddPollingUnitView(View):
    def get(self, request):
        form = PollingUnitForm()
        return render(request, 'create_polling_unit.html', {'form': form})

    def post(self, request):
        form = PollingUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polling_unit_list')
        return render(request, 'create_polling_unit.html', {'form': form})
    
def filter_page(request):
    lgas = Lga.objects.all()
    wards = Ward.objects.all()
    polling_units = PollingUnit.objects.all()
    context = {
        'lgas': lgas,
        'wards': wards,
        'polling_units': polling_units,
    }
    return render(request, 'filter_page.html', context)

def lga_results_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        lga_id = request.GET.get('lga_id')
        try:
            lga = Lga.objects.get(id=lga_id)
            polling_units = PollingUnit.objects.filter(lga_id=lga_id)
            unique_ids = polling_units.values_list('uniqueid', flat=True)
            results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid__in=unique_ids)

            wards = Ward.objects.values_list('ward_id', flat=True)
            polling_units = PollingUnit.objects.values_list('unique_id', flat=True)
            context = {
                'wards': wards,
                'polling_units': polling_units,
            }

            summed_results = {}
            for result in results:
                party_abbreviation = result.party_abbreviation
                party_score = result.party_score
                if party_abbreviation not in summed_results:
                    summed_results[party_abbreviation] = {
                        'party_abbreviation': party_abbreviation,
                        'total_party_score': party_score,
                        'results': [result],
                    }
                else:
                    summed_results[party_abbreviation]['total_party_score'] += party_score
                    summed_results[party_abbreviation]['results'].append(result)
            
            summed_results_list = list(summed_results.values())
            
            context = {
                'summed_results': summed_results_list,
            }
            
            results_table_html = render_to_string('results_table.html', context)
            
            return JsonResponse({'results_table_html': results_table_html})
        except Lga.DoesNotExist:
            pass
    # If not an AJAX GET request, render the initial page with the select box
    lgas = Lga.objects.all()
    context = {
        'lgas': lgas,
    }
    return render(request, 'select_lga.html', context)