"""urlpatterns for the rse Django app."""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from rse.views import *


urlpatterns = [
    # main site index
    # ex: /training
    url(r'^$', index.index, name='index'),

    #######################
    ### Authentication ####
    #######################
    
    # Login using built in auth view
    url(r'^login/?$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    # Logout using built in auth view
    url(r'^logout/?$', auth_views.LogoutView.as_view(), name='logout'),
    
    # change password using built in auth view
    url(r'^changepassword/?$', auth_views.PasswordChangeView.as_view(template_name='changepassword.html', success_url=reverse_lazy('index')), name='change_password'),
    
    # New user (choose type) view
    url(r'^user/new/?$', authentication.user_new, name='user_new'),
    
    # New rse user view
    url(r'^user/new/rse?$', authentication.user_new_rse, name='user_new_rse'),
    
    # Edit rse user
    url(r'^user/edit/rse/(?P<rse_id>[0-9]+)?$', authentication.user_edit_rse, name='user_edit_rse'),
    
    # New admin user view
    url(r'^user/new/admin?$', authentication.user_new_admin, name='user_new_admin'),
    
    # Edit admin user view
    url(r'^user/edit/admin/(?P<user_id>[0-9]+)?$', authentication.user_edit_admin, name='user_edit_admin'),
    
    # User change password view
    url(r'^user/changepassword/(?P<user_id>[0-9]+)?$', authentication.user_change_password, name='user_change_password'),
    
    # View all users (RSE and admin)
    url(r'^users?$', authentication.users, name='users'),


    ################################
    ### Projects and Allocations ###
    ################################

    # View All Projects (list view)
    url(r'^projects$', projects.projects, name='projects'),

    # Create Allocated Project view
    url(r'^project/new$', projects.project_new, name='project_new'),

    # Create Allocated Project view
    url(r'^project/allocated/new$', projects.project_new_allocated, name='project_new_allocated'),
    
    # Create Service Project view
    url(r'^project/service/new$', projects.project_new_service, name='project_new_service'),

    # Project view
    url(r'^project/(?P<project_id>[0-9]+)$', projects.project, name='project'),
      
    # Edit Project view
    url(r'^project/edit/(?P<project_id>[0-9]+)$', projects.project_edit, name='project_edit'),
    
    # Project allocation view
    url(r'^project/(?P<project_id>[0-9]+)/allocations$', projects.project_allocations, name='project_allocations'),

    # Project allocation edit view
    url(r'^project/(?P<project_id>[0-9]+)/allocations/edit$', projects.project_allocations_edit, name='project_allocations_edit'),
    
    # Allocation delete (forwards to project allocation view)
    url(r'^project/allocations/delete/(?P<pk>[0-9]+)$', projects.project_allocations_delete.as_view(), name='project_allocations_delete'),
    url(r'^project/allocations/delete/$', projects.project_allocations_delete.as_view(), name='project_allocations_delete_noid'), # trailing id version for dynamically (JS) constructed urls
    
    # Project delete
    url(r'^project/delete/(?P<pk>[0-9]+)$', projects.project_delete.as_view(), name='project_delete'),
    

    ###############
    ### Clients ###
    ###############

    # View All Clients (list view)
    url(r'^clients$', clients.clients, name='clients'),
    
    # View a client (and associated projects)
    url(r'^client/(?P<client_id>[0-9]+)$', clients.client, name='client'),
    
    # Add a new client
    url(r'^client/new$', clients.client_new, name='client_new'),
    
    # Edit a client (and associated projects)
    url(r'^client/edit/(?P<client_id>[0-9]+)$', clients.client_edit, name='client_edit'),
    
    # Edit a client (and associated projects)
    url(r'^client/delete/(?P<pk>[0-9]+)$', clients.client_delete.as_view(), name='client_delete'),


    ############
    ### RSEs ###
    ############

    # View a single RSE
    url(r'^rse/(?P<rse_username>[\w.@+-]+)$', rses.rse, name='rse'),
    
    # RSE view list
    url(r'^rses$', rses.rses, name='rses'),
        
    # RSE allocation view by rse id
    url(r'^rse/id/(?P<rse_id>[0-9]+)$', rses.rseid, name='rseid'),
    url(r'^rse/id/$', rses.rseid, name='rseid'),  # without id parameter for dynamically constructed queries
          
    # RSE team commitment view all
    url(r'^commitment$', rses.commitment, name='commitment'),

    # RSE salary grade change view
    url(r'^rse/(?P<rse_username>[\w.@+-]+)/salary$', rses.rse_salary, name='rse_salary'),

    # RSE salary grade change delete
    url(r'^rse/salarychange/delete/(?P<pk>[0-9]+)$', rses.rse_salarygradechange_delete.as_view(), name='rse_salarygradechange_delete'),
    url(r'^rse/salarychange/delete/$', rses.rse_salarygradechange_delete.as_view(), name='rse_salarygradechange_delete_noid'), # trailing id version for dynamically (JS) constructed urls

    # AJAX salary band options by year
    url(r'^ajax/salaryband$', rses.ajax_salary_band_by_year, name='ajax_salary_band_by_year'),    
    
        
    #################################
    ### Salary and Grade Changes ####
    #################################
    
    # View Salary Bands (by financial year) - view all financial years
    url(r'^financialyears$', salary.financialyears, name='financialyears'),

    # Edit Salary Bands (by financial year)
    url(r'^financialyear/edit/(?P<year_id>[0-9]+)$', salary.financialyear_edit, name='financialyear_edit'),

    # Create a new financial year
    url(r'^financialyear/new$', salary.financialyear_new, name='financialyear_new'),

    # Create a new financial year
    url(r'^financialyear/delete/(?P<pk>[0-9]+)$', salary.financialyear_delete.as_view(), name='financialyear_delete'),
    
    # Edit Salary Bands (by financial year) - add a salary band
    url(r'^salaryband/edit/(?P<sb_id>[0-9]+)$', salary.salaryband_edit, name='salaryband_edit'),

    # Salary Band delete (forwards to current financial year view)
    url(r'^salaryband/delete/(?P<pk>[0-9]+)$', salary.financialyear_salaryband_delete.as_view(), name='financialyear_salaryband'),
    url(r'^salaryband/delete/$', salary.financialyear_salaryband_delete.as_view(), name='financialyear_salaryband_delete_noid'), # trailing id version for dynamically (JS) constructed urls
    
    
    ##################
    ### Reporting ####
    ##################
    
    # View current cost distribution (staff charging)
    url(r'^allocations/recent$', reporting.allocations_recent, name='allocations_recent'),

    # View current cost distribution (staff charging)
    url(r'^costdistributions$', reporting.costdistributions, name='costdistributions'),

    # View projected cost distribution (for an individual)
    url(r'^costdistribution/(?P<rse_username>[\w.@+-]+)$', reporting.costdistribution, name='costdistribution'),

    # View rses staff costs summary
    url(r'^rses/staffcosts$', reporting.rses_staffcosts, name='rses_staffcosts'),

    # View rses staff costs summary
    url(r'^rse/(?P<rse_username>[\w.@+-]+)/staffcost$', reporting.rse_staffcost, name='rse_staffcost'),

    # View service projects and invoice status
    url(r'^service/income/outstanding$', reporting.serviceoutstanding, name='serviceoutstanding'),

    # View service income
    url(r'^service/income/summary$', reporting.serviceincome, name='serviceincome'),

    # View allocated project income summary
    url(r'^projects/income/summary$', reporting.projects_income_summary, name='projects_income_summary'),

    # View for breakdown of staff cost calculations
    url(r'^project/(?P<project_id>[0-9]+)/staffcosts$', reporting.project_staffcosts, name='project_staffcosts'),

    # AJAX query to get remain time on project for a given RSE (based off salary project)
    url(r'^project/budget/remainingdays/(?P<project_id>[0-9]+)/(?P<rse_id>[0-9]+)/(?P<start>\d{2}-\d{2}-\d{4})/(?P<percent>\d+(?:\.\d+)?)$', reporting.project_remaining_days, name='project_remaining_days'),  # accepts int or float percent value
    url(r'^project/budget/remainingdays$', reporting.project_remaining_days, name='project_remaining_days'), # no id version for dynamically constructed urls

    # View allocated project income summary
    url(r'^projects/internal/summary$', reporting.projects_internal_summary, name='projects_internal_summary'),

    # View allocated project income summary
    url(r'^financialsummary$', reporting.financial_summary, name='financial_summary'),

]
