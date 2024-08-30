import colorama
from colorama import Fore, Back, Style

# If using Windows, init() will cause anything sent to stdout or stderr
# will have ANSI color codes converted to the Windows versions. Hooray!
# If you are already using an ANSI compliant shell, it won't do anything
colorama.init()

FORMATTING = 23

def modifiedBubbleSort(arr):
    n = len(arr)
    swapped = True
    swapsTotal = 0
    start = 0
    end = n-1
    print(f"{'Initial Array:':<{FORMATTING}} {'[' + ', '.join([str(x) for x in arr]) + ']'}")
   # print('[' + ', '.join([str(x) for x in arr]) + ']')
    while (swapped == True):
        # reset the swapped flag
        # when entering the loop
        # because it might be true from a previous iteration
        swapped = False
        print('-' * 47)
        swapCount = 0
        for i in range(start, end):

            if (arr[i] > arr[i+1]):
                arr[i], arr[i+1] = arr[i+1], arr[i]
                swapped = True
                swapsTotal += 1
                swapCount += 1
                print(f"{f'Right-to-Left Swap #{swapCount}:':<{FORMATTING}} {'[' + ', '.join([Fore.RED + str(x) + Style.RESET_ALL if x ==arr[i+1] else Fore.GREEN + str(x) + Style.RESET_ALL if x==arr[i] else str(x) for x in arr]) + ']'}")

        # if nothing moved, then array is sorted.
        if (swapped == False):
            break

        # otherwise, reset the swapped flag so that it
        # can be used in the next stage
        swapped = False
        swapCount = 0

        # move the end point back by one, because
        # item at the end is in its rightful spot
        end = end-1
        print('-' * 47)
        # from right to left, doing the same
        # comparison as in the previous stage

        for i in range(end-1, start-1, -1):

            if (arr[i] > arr[i+1]):

                arr[i], arr[i+1] = arr[i+1], arr[i]
                swapped = True
                swapCount += 1
                swapsTotal += 1

                print(f"{f'Left-to-Right Swap #{swapCount}:':<{FORMATTING}} {'[' + ', '.join([Fore.GREEN + str(x) + Style.RESET_ALL if x ==arr[i+1] else Fore.RED + str(x) + Style.RESET_ALL if x==arr[i] else str(x) for x in arr]) + ']'}")

        # increase the starting point, because
        # the last stage would have moved the next
        # smallest number to its rightful spot.
        start = start+1

    return (swapsTotal)

def main():
    arr = [6, 5, 4, 3, 2, 1]
    swaps = modifiedBubbleSort(arr)
    print(f"{'Sorted Array:':<{FORMATTING}} {'[' + ', '.join([str(x) for x in arr]) + ']'}")

    print()
    print(f"Swaps: {swaps}")

if __name__=="__main__":
    main()
