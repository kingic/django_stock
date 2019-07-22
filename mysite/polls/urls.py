from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),                       # django 예제
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),            # django 예제
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),  # django 예제
    path('<int:question_id>/vote/', views.vote, name='vote'),                # django 예제
    path('history/', views.history, name='history'),                         # K-FS 예제
    path('company00/', views.company00, name='company00'),                   # K-FS 예제
    path('company01/', views.company01, name='company01'),                   # K-FS 예제
    path('company02/', views.company02, name='company02'),                   # K-FS 예제
    path('business00/', views.business00, name='business00'),                # K-FS 예제
    path('stock/', views.stock_result, name='stockwatch'),                    # 초기 화면
    path('stock_result', views.stock_result, name='stockwatch_result'),     # 검색 결과 rendering 화면
    path('side', views.search_by_ic, name='side'),
    #path('stock_add', views.db_add, name='db_update'),
    # stock_add 는 초기에 DB에 모든 종목 넣는 용도로 사용.(한번만 사용하고 주석으로 잠그자)

]