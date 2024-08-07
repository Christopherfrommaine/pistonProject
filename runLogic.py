from fileHelperFunctions import *
import conversion


def runWithoutManualCorrection(door, pistonLayout='original', logging=False):
    runBeforeManualCorrections(door, pistonLayout, logging)
    runAfterManaualCorrections(pistonLayout, logging)


def runBeforeManualCorrections(door, pistonLayout='original', logging=False):
    log = ''
    if logging:
        odoor = door.originalState
        log += str(odoor) + '\n'
        for m in door.moves:
            odoor.applyMove(m)
            log += str(odoor) + '\n'

    try:
        originalMoves = door.moves

        log += f'original moves: {originalMoves}\n'

        # Apply Corrections
        correctedMoves = conversion.applyCorrections(originalMoves, door.originalState)

        log += f'corrected moves: {correctedMoves}\n'

        # Numerical Layout Translation
        layoutNumberedRules = conversion.toLayoutMoves(correctedMoves, pistonLayout)

        log += f'layout numbered rules: {layoutNumberedRules}\n'

        writeToFile(str(layoutNumberedRules).replace(' ', '\n'), 'algorithmOutput.txt')

    except Exception as e:
        if logging:
            writeToFile(log, projectDirectory + 'debugging/log.txt')
        raise e

    if logging:
        writeToFile(log, projectDirectory + 'debugging/log.txt')

def runAfterManaualCorrections(pistonLayout='original', logging=False, readFromFilePath='algorithmOutput.txt', worldName=None):
    log = readFromFile(projectDirectory + 'debugging/log.txt')

    if worldName is None:
        if pistonLayout == 'original':
            worldName = '24xInfinity Door 2-21-23'
        elif pistonLayout == 'new':
            worldName = 'Piston Door Algorithem'

    try:
        # Get Moves from File
        manuallyCorrectedMoves = readMovesFromFile(readFromFilePath)

        log += f'manually corrected moves: {manuallyCorrectedMoves}\n'

        # Layout Conversion
        commands = conversion.toLayoutCommands(manuallyCorrectedMoves, pistonLayout)

        log += f'outputted commands: {commands}\n'

        writeToMinecraftDatapack(commands, worldName)

    except Exception as e:
        if logging:
            writeToFile(log, projectDirectory + 'debugging/log.txt')
        raise e

    if logging:
        writeToFile(log, projectDirectory + 'debugging/log.txt')
