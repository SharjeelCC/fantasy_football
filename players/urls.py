from django.urls import path
from players.views import ListPlayerForSaleView, PlayersForSaleListView, PlayerTransferView, TransactionHistoryView

urlpatterns = [
    path('<int:player_id>/list-for-sale/', ListPlayerForSaleView.as_view(), name='list-player-for-sale'),
    path('for-sale/', PlayersForSaleListView.as_view(), name='players-for-sale'),
    path('transfer/<int:player_id>/', PlayerTransferView.as_view(), name='player-transfer'),
    path('transactions/', TransactionHistoryView.as_view(), name='transaction-history')
]
