from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .renderers import PlainTextRenderer
from TicTacGame.TicTacLogic import Board

# Create your views here.
class TicTac(APIView):
    """
    View that makes decisions based on the board state and returns a new board state in text.

    * Requires no authentication.
    * Requires no permission.
    """
    renderer_classes = (PlainTextRenderer, )    

    def get(self, request, format=None):
        #Get current board state        
        board_string = request.query_params.get('board', None)
        
        if board_string is None:
            return Response ('', status=status.HTTP_400_BAD_REQUEST)

        #instantiate a new game board
        game = Board(board_string, 'x', 'o', ' ')
        
        #check if board is valid
        if not game.validBoard():
            return Response (board_string, status=status.HTTP_400_BAD_REQUEST) 
        
        #make a play
        play = game.makeMove()
                
        return Response(play, status=status.HTTP_200_OK)