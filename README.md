# Unicode chess game

Chess game coded in Python

## Rules

### Check

- When a king is under immediate attack

### Checkmate

- When a king is in check and there is no legal moves to get out of the check

### Pawn promotion

- When a pawn advances to its eight rank, as part of the move
- Is currently exchanged for a queen

### Castling

**TODO**

- Neither the king nor the rook has previously moved during the game
- there are no pieces between the king and the rook
- the king is not in check, and will not pass through or land on any square attacked by an enemy piece
- (castling is permitted if the rook is under attack)

### En passant

**TODO**

- When a pawn makes a two-step advance from its starting position and there is an opponent's pawn on a square
next ot the destination square on an adjacent file, then the opponent's pawn can capture it, moving to the
square the pawn passed over. This can only be done on the very next turn, otherwise the right to do so is
forfeited

### Draw Conditions

- Stalemate: if the player on turn that has no legal moves, but is not in check
- Fifty-move rule

### Scoring

**TODO**
