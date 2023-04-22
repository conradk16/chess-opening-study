import pandas as pd
import numpy as np
import chess
import chess.svg
from random import shuffle
from IPython.display import clear_output
from time import sleep
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_df():
    with open('sheet_name.txt', 'r') as f:
        sheet_name = f.read()
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(credentials)
    sheet = client.open(sheet_name)
    white_values = sheet.worksheet('White').get_all_values()
    black_values = sheet.worksheet('Black').get_all_values()
    values = white_values + black_values
    df = pd.DataFrame(values).replace('', np.nan)
    #df[df.columns.stop] = np.nan # add an extra column for name purposes
    return df

def get_board_and_next_move(moves, is_white):
    board = chess.Board()
    for move in moves[:-1]:
        try:
            board.push_san(move)
        except Exception as e:
            raise ValueError(f'moves: {str(moves)}, move: {str(move)}, error: {e}')
    return board, moves[-1]

def get_move_display(moves):
    str_parts = ['\n']
    currently_on_move = 1
    current_player = 'w'
    for move in moves:
        if current_player == 'w':
            str_parts.append(str(currently_on_move) + '. ' + move)
            current_player = 'b'
        else:
            str_parts.append(str(currently_on_move) + '...' + move + '\n')
            currently_on_move += 1
            current_player = 'w'
    if len(str_parts) != 0 and len(str_parts) % 2 == 1: # not empty board and ended on black
        str_parts[-1] = str_parts[-1][:-1] # drop the last newline
    return ' '.join(str_parts) if len(str_parts) > 1 else '[]'

def display_board(board, is_white, opening):
    print(get_move_display(opening[:-1]))

    kwargs = {'size': 400}
    if len(opening) != 1:
        kwargs['lastmove'] = board.peek()
    if not is_white:
        kwargs['orientation'] = chess.BLACK
    
    display(chess.svg.board(board, **kwargs))

def get_all_openings():
    df = get_df()
    
    # fill in missing squares
    new_rows = []
    new_rows.append(df.iloc[0].to_dict())
    for index, row in df.iloc[1:].iterrows():
        new_row = {}
        for i in range(len(row)):
            if not pd.isna(row[i]) and (row[i][0].isdigit() or row[i] == '#'):
                new_row[i] = row[i]
                break
            else:
                new_row[i] = new_rows[-1][i]
        new_rows.append(new_row)
    new_df = pd.DataFrame(new_rows)
    
    # convert each opening to a dictionary with a list of moves
    openings = []
    for _, row in new_df.iterrows():
        row = ' '.join([x for x in row.tolist() if not pd.isna(x) and x[0].isdigit()]).split(' ')
        moves = []
        duplicate = False
        for move in row:
            if '...' in move:
                move = move.split('...')[1]
            else:
                move = move.split('.')[1]
            if '#' in move:
                duplicate = True
            moves.append(move)
        if not duplicate:
            openings.append(moves)
    
    return openings

def get_openings_subset(is_white, starting_opponent_move_lists):
    all_openings = get_all_openings()
    openings_subset = []
    for opening in all_openings:
        if (is_white and len(opening) % 2 == 0) or (not is_white and len(opening) % 2 == 1):
            continue
        found_match = False
        for starting_opponent_moves in starting_opponent_move_lists:
            success = True
            for i, move in enumerate(starting_opponent_moves):
                move_index = 2 * i + 1 if is_white else 2 * i
                if move_index >= len(opening) or opening[move_index] != move:
                    success = False
                    break
            if success:
                found_match = True
                break
        if found_match:
            openings_subset.append(opening)
    return openings_subset

def train(is_white=True, starting_opponent_move_lists=[[]], shuffle_moves=True):
    working_on = get_openings_subset(is_white, starting_opponent_move_lists)
    while len(working_on) > 0:
        if shuffle_moves:
            shuffle(working_on)
        num_correct = 0
        num_completed = 0
        new_working_on = []
        for opening in working_on:
            is_white = False
            if len(opening) % 2 == 1:
                is_white = True
            board, next_move = get_board_and_next_move(opening, is_white)
            display_board(board, is_white, opening)
            sleep(0.01)
            x = input()
            num_completed += 1
            clear_output()
            board.push_san(next_move)
            display_board(board, is_white, opening)
            if x == next_move:
                num_correct += 1
                print(f'nice! {num_correct}/{num_completed}')
            else:
                print(f'you played {x}, but correct move was {next_move}')
                new_working_on.append(opening)
            print(f'set size: {len(working_on)}')
            print('press enter to continue')
            input()
            clear_output()

        print(f'you got {num_correct} / {num_completed}')
        print('press enter to continue')
        input()
        clear_output()
        working_on = new_working_on
    print('done!')




