from fileHelperFunctions import *
import conversion
import simplification
import simplify2
from  algorithm import State


def runWithoutManualCorrection(door, pistonLayout='original', logging=False, worldName=None, simplification1=False, simplification2=False, prnt=False, rep=True, CARS=False):
    runBeforeManualCorrections(door, pistonLayout, logging, simplification1, simplification2, prnt, rep, CARS)
    runAfterManaualCorrections(pistonLayout, logging, worldName=worldName)


def runBeforeManualCorrections(door: State, pistonLayout='original', logging=False, simplification1=False, simplification2=False, prnt=False, rep=True, CARS=False):
    if logging:
        writeToFile('', projectDirectory + 'debugging/log.txt')

    log = ''
    logErrorPostfix = ''

    try:
        odoor = door.originalState
        log += f'{odoor}\n'
        
        for movei, move in enumerate(door.moves):
            odoor.applyMove(move)
            log += f'{odoor} | {movei} | {move}\n'

        originalMoves = door.moves

        log += f'original moves: {originalMoves}\n'

        # Apply Simplifications First
        simpMoves1 = simplification.simplifyUncorrectedMoves(originalMoves, door) if simplification1 else originalMoves

        simpMoves1 = simplify2.repeatSimplification(simpMoves1, door.originalState, simplify2.contextAwareReplacementSimplification) if CARS else simpMoves1

        log += f'simp moves: {simpMoves1}\n'

        # Apply Corrections
        correctedMoves = conversion.applyCorrections(simpMoves1, door.originalState)

        log += f'corrected moves: {correctedMoves}\n'

        # Apply Simplifications Second
        simpMoves2 = simplification.simplifyCorrectedMoves(correctedMoves) if simplification2 else correctedMoves

        log += f'simp moves 2: {simpMoves2}\n'

        # Numerical Layout Translation
        layoutNumberedRules = conversion.toLayoutMoves(simpMoves2, pistonLayout)

        log += f'layout numbered rules: {layoutNumberedRules}\n'

        # Apply Door Replacements
        replacedRules = simplification.repLayoutMoves(layoutNumberedRules) if rep else layoutNumberedRules

        if prnt:
            print(replacedRules)

        writeToFile(str(replacedRules), 'algorithmOutput.txt')

    except Exception as e:
        if logging:
            logString(log + logErrorPostfix)
        raise e

    if logging:
        logString(log)

def runAfterManaualCorrections(pistonLayout='original', logging=False, readFromFilePath='algorithmOutput.txt', worldName=None):
    log = ''

    if worldName is None:
        if pistonLayout == 'original':
            worldName = '24xInfinity Door 2-21-23'
        elif pistonLayout == 'new':
            worldName = 'Piston Door Algorithem'
        elif pistonLayout == 'shulker':
            worldName = 'Piston Door Algorithem'

    try:
        # Get Moves from File
        manuallyCorrectedMoves = readMovesFromFile(readFromFilePath)

        log += f'manually corrected moves: {manuallyCorrectedMoves}\n'

        # Layout Conversion
        commands = conversion.toLayoutCommands(manuallyCorrectedMoves, pistonLayout, logging)

        log += f'outputted commands: ' + str(commands) + '\n'

        writeToMinecraftDatapack(commands, worldName)

    except Exception as e:
        if logging:
            logString(log) 
        raise e

    if logging:
        logString(log)
