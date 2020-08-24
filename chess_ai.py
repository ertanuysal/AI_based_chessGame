import chess

"""
These tables represent value of location for each pieces and determined values by experts
For example:
it makes sense that the pawn's score increases 
as it approaches the opposite side.
Knight have fewer points around edge because of poor mobility.
"""
pawntable = [
 0,  0,  0,  0,  0,  0,  0,  0,
 5, 10, 10,-20,-20, 10, 10,  5,
 5, -5,-10,  0,  0,-10, -5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5,  5, 10, 25, 25, 10,  5,  5,
10, 10, 20, 30, 30, 20, 10, 10,
50, 50, 50, 50, 50, 50, 50, 50,     
 0,  0,  0,  0,  0,  0,  0,  0]

knightstable = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  5,  5,  0,-20,-40,
-30,  5, 10, 15, 15, 10,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 10, 15, 15, 10,  0,-30,
-40,-20,  0,  0,  0,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50]

bishopstable = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  5,  0,  0,  0,  0,  5,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10,-10,-10,-10,-10,-20]

rookstable = [
  0,  0,  0,  5,  5,  0,  0,  0,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  5, 10, 10, 10, 10, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]

queenstable = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  5,  5,  5,  5,  5,  0,-10,
  0,  0,  5,  5,  5,  5,  0, -5,
 -5,  0,  5,  5,  5,  5,  0, -5,
-10,  0,  5,  5,  5,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]

kingstable = [
 20, 30, 10,  0,  0, 10, 30, 20,
 20, 20,  0,  0,  0,  0, 20, 20,
-10,-20,-20,-20,-20,-20,-20,-10,
-20,-30,-30,-40,-40,-30,-30,-20,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30]



def FirstMove(depth, board,trueOrFalse,depthOfBoard):
    compare = -9999 # for comparing first value and first variable is too small because fist value should be max 
    finalPath = None
    depth=depthOfBoard 
    
    for x in board.legal_moves:
        if board.legal_moves.count()==1: # if there is only one move,make it.
            return x
        
        move = chess.Move.from_uci(str(x))
        
        board.push(move) #make x legal move 
    
        value = max(compare,calculateMinimax(depth - 1, board, not trueOrFalse,depthOfBoard))
        board.pop() #undo movement and get back to root
        
        result= findBest(value,compare,finalPath,move)
        
        compare=result[0]
        finalPath=result[1]
        
    return finalPath

def findBest(value,compare,finalPath,move):
    if( value > compare): # if value is max,that become best move path
            compare = value #each 
            finalPath = move
    return compare, finalPath

def calculateMinimax(depth, board, trueOrFalse,depthOfBoard):
    
    if(depth == 0):
        return evaluation(board) #after reach deepst value in tree,we need to calculate values(using evaluation function)
    possibleMoves = board.legal_moves
    if(trueOrFalse==True): #this condition uses to determined max()  or min() of node
        compare=-9999
        
        for x in possibleMoves: #possible moves in that depth
            
            move = chess.Move.from_uci(str(x))
            board.push(move)
            #Recursive method uses for depth fist search algorithm.
            #It provide to reach deepest values in tree.After find these value ,
            #we compare which one is maximum/minimum.
            #recursive call change calculation type (max() or min())
            compare = max(compare,calculateMinimax(depth - 1, board, False,depthOfBoard))
            board.pop()
        
        if board.is_checkmate():
            return -(depth/depthOfBoard*700000000)    #if there is a checkmade in this depth,these path earn points
        return compare                            #and checkmate which is with less move,earning more point
    else:
        compare=9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            compare = min(compare, calculateMinimax(depth - 1, board, True,depthOfBoard))
            board.pop()
        if board.is_checkmate():
            return (depth/depthOfBoard*700000000)
        return compare

def checkMadeControlInDepthTrue(board,depth,bestMove):
    if(board.is_checkmate()): # Is there any checkmade in this depth?
        return True
    else:
        return False
    
def checkMadeControlInDepthFalse(board,depth,bestMove):
    if(board.is_checkmate()): # Is there any checkmade in this depth?
        return True
    else:
        return False
    
def evaluation(board):
    piece=[chess.PAWN,chess.BISHOP,chess.ROOK,chess.QUEEN,chess.KNIGHT] #define piece name in array
    i=0
    result=0   # evalation function result
    valueOfPiece=[100,350,500,1000,350]; #point of each piece for example:pawn=100 point.
    
    if board.is_checkmate (): # Is there any checkmade in deepest nodes?
        if board.turn:
            return -99999;
        else:
            return 99999;
      
    if(board.is_stalemate()): #means game ends in draw.
        return 0;
       
    for x in piece:
        whitePiece = len(board.pieces(x, chess.WHITE)) #number of white pieces
        blackPiece = len(board.pieces(x, chess.BLACK)) # number of black pieces
        result =result + ((whitePiece-blackPiece) * valueOfPiece[i]) #calculate "material" depends on piece values.
        i=i+1
    
    WhiteLocationPawn=0
    BlackLocationPawn=0
    pawnPointInLocation=0
    
    whiteLocationKnight=0
    blackLocationKnight=0
    knightPointInLocation=0
    
    whiteLocationBishop=0
    blackLocationBishop=0
    bishopPointInLocation=0
    
    whiteLocationRook=0
    blackLocationRook=0
    rookPointInLocation=0
    
    whiteLocationQueen=0
    blackLocationQueen=0
    queenPointInLocation=0
    
    whiteLocationKing=0
    blackLocationKing=0
    kingPointInLocation=0
    
    
    for i in board.pieces(chess.PAWN,chess.WHITE): #check is there any pawn in that location
        WhiteLocationPawn += pawntable[i] # total value of white pawn accorging to table
    for i in board.pieces(chess.PAWN,chess.BLACK):
        BlackLocationPawn+=pawntable[chess.square_mirror(i)] # location value is opposite for black player
        pawnPointInLocation=WhiteLocationPawn-BlackLocationPawn #calculate availability of position
    
    for i in board.pieces(chess.KNIGHT,chess.WHITE):
        whiteLocationKnight += knightstable[i]
    for i in board.pieces(chess.KNIGHT,chess.BLACK):
        blackLocationKnight+=knightstable[chess.square_mirror(i)]
    knightPointInLocation=whiteLocationKnight-blackLocationKnight
    
    for i in board.pieces(chess.BISHOP,chess.WHITE):
        whiteLocationBishop += bishopstable[i]
    for i in board.pieces(chess.BISHOP,chess.BLACK):
        blackLocationBishop+=bishopstable[chess.square_mirror(i)]
    bishopPointInLocation=whiteLocationBishop-blackLocationBishop
    
        
    for i in board.pieces(chess.ROOK,chess.WHITE):
        whiteLocationRook += rookstable[i]  
    for i in board.pieces(chess.ROOK,chess.BLACK):
        blackLocationRook+=rookstable[chess.square_mirror(i)]
    rookPointInLocation=whiteLocationRook-blackLocationRook
    
    for i in board.pieces(chess.QUEEN,chess.WHITE):
        whiteLocationQueen += queenstable[i]
    for i in board.pieces(chess.QUEEN,chess.BLACK):
        blackLocationQueen+=queenstable[chess.square_mirror(i)]
    queenPointInLocation=whiteLocationQueen-blackLocationQueen
    
    for i in board.pieces(chess.KING,chess.WHITE):
        whiteLocationKing += kingstable[i]
    for i in board.pieces(chess.KING,chess.BLACK):
        blackLocationKing+= kingstable[chess.square_mirror(i)]
    kingPointInLocation=whiteLocationKing-blackLocationKing
    
    #evaluation function result with using "material function" and "piece value calculation with location" methods
    #In order to provide 
    result = result + (kingPointInLocation + queenPointInLocation +rookPointInLocation +bishopPointInLocation +knightPointInLocation +pawnPointInLocation)
    
    
    return result
        
def ai_play(board):
    depthOfBoard=4; # this variable indicates how many steps it will look up to.in tree
    plays = [] # for keeping legal move of rootNode
    movees=FirstMove(depthOfBoard,board,True,depthOfBoard)
    counter = 0

    for play in board.legal_moves:
        plays.append(str(play))  
        if(movees == play): # if best move is legal move,find move in plays array and  make it
            return plays[counter]
        counter +=1
	 


