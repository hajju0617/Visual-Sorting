import os
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame               # pygame
from math import floor

pygame.init()
pygame.display.set_caption("Visual-Sorting")
screensize = (1280, 720)
screen = pygame.display.set_mode(screensize)
clock = pygame.time.Clock()
framerate = 10
running = True

font = pygame.font.Font(None, 30)

data_size = 128             # 정렬할 데이터의 개수   
data = list()
data_color = list()

# 랜덤 데이터 생성.
def DataGenerator():        
    global data
    global data_color
    data = [random.randint(10, 400) for _ in range(data_size)]
    data_color = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(data_size)]

DataGenerator()

def RenderMultilineText(text, font, color, x, y, line_height):
    for i, line in enumerate(text.splitlines()):
        line_surf = font.render(line, True, color)
        screen.blit(line_surf, (x, y + i * line_height))

# 시각화 함수.
def Visualize():            
    screen.fill("black")

    RenderMultilineText(
        "Sorting Visualization\n\n"
        "*q: Quick Sorting [ O(nlogn) ]\n"
        "*m: Merge Sorting (Visual O) [ O(nlogn) ]\n"
        "*n: Merge Sorting (Visual X) [ O(nlogn) ]\n"
        "*h: Heap Sorting [ O(nlogn) ]\n"
        "\n*g: Random Data Generation",
        font,
        "gray",
        20,
        10,
        25
    )

    for i in range(data_size):
        pygame.draw.rect(screen, data_color[i], (i*10, screensize[1]-data[i], 10, data[i]))

    pygame.display.flip()
    clock.tick(framerate)

def Finalize():
    screen.fill("white")
    pygame.display.flip()
    clock.tick(framerate)

def EventHandler():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return -1
        elif event.type == pygame.QUIT:
            return -1
    return 0

# 퀵 정렬.
def QuickSort(start, end):
    if start >= end:
        return 0

    pivot = start
    left = start + 1
    right = end

    while left <= right:
        if EventHandler() == -1:
            return -1

        while left <= end and data[left] <= data[pivot]:
            left += 1
        while right > start and data[right] >= data[pivot]:
            right -= 1
        if left > right:
            data[right], data[pivot] = data[pivot], data[right]
            data_color[right], data_color[pivot] = data_color[pivot], data_color[right]
        else:
            data[left], data[right] = data[right], data[left]
            data_color[left], data_color[right] = data_color[right], data_color[left]

        Visualize()

    if QuickSort(start, right - 1) == -1:
        return -1
    if QuickSort(right + 1, end) == -1:
        return -1
    return 0

# 합병 정렬 (정렬 과정을 실시간으로 확인 가능)
def MergeSort_2():
    def sort(low, high):
        if EventHandler() == -1:
            return -1
        if high - low < 2:
            return 0

        mid = (low + high) // 2
        if sort(low, mid) == -1:
            return -1
        if sort(mid, high) == -1:
            return -1
        if merge(low, mid, high) == -1:
            return -1
        return 0

    def merge(low, mid, high):
        data_temp = list()
        color_temp = list()
        l, h = low, mid

        while l < mid and h < high:
            if data[l] < data[h]:
                data_temp.append(data[l])
                color_temp.append(data_color[l])
                l += 1
            else:
                data_temp.append(data[h])
                color_temp.append(data_color[h])
                h += 1

        while l < mid:
            data_temp.append(data[l])
            color_temp.append(data_color[l])
            l += 1

        while h < high:
            data_temp.append(data[h])
            color_temp.append(data_color[h])
            h += 1

        for i in range(low, high):
            data[i] = data_temp[i - low]
            data_color[i] = color_temp[i - low]
            Visualize()
            if EventHandler() == -1:
                return -1

        return 0

    sort(0, data_size)

# 합병 정렬 (정렬 전/후 모습만 확인 가능)
def MergeSort_1(data_list, color_list):
    if len(data_list) < 2:
        return data_list, color_list

    mid = len(data_list) // 2
    low_data_list, low_color_list = MergeSort_1(data_list[:mid], color_list[:mid])
    high_data_list, high_color_list = MergeSort_1(data_list[mid:], color_list[mid:])

    merged_data_list = list()
    merged_color_list = list()
    l = h = 0
    while l < len(low_data_list) and h < len(high_data_list):
        if low_data_list[l] < high_data_list[h]:
            merged_data_list.append(low_data_list[l])
            merged_color_list.append(low_color_list[l])
            l += 1
        else:
            merged_data_list.append(high_data_list[h])
            merged_color_list.append(high_color_list[h])
            h += 1

    merged_data_list += low_data_list[l:]
    merged_color_list += low_color_list[l:]
    merged_data_list += high_data_list[h:]
    merged_color_list += high_color_list[h:]

    return merged_data_list, merged_color_list

# 힙 정렬.
def HeapSort():
    for i in range(len(data)):
        par = floor((i - 1) / 2)
        while par >= 0 and data[par] < data[i]:
            data[par], data[i] = data[i], data[par]
            data_color[par], data_color[i] = data_color[i], data_color[par]
            i = par
            par = floor((i - 1) / 2)

    for i in range(len(data)-1, 0, -1):
        data[0], data[i] = data[i], data[0]
        data_color[0], data_color[i] = data_color[i], data_color[0]

        cur = 0
        lch = 1
        rch = 2

        while True:
            if EventHandler() == -1:
                return

            if rch < i and data[lch] < data[rch]:
                lch = rch

            if lch < i and data[lch] > data[cur]:
                data[lch], data[cur] = data[cur], data[lch]
                data_color[lch], data_color[cur] = data_color[cur], data_color[lch]

                Visualize()

                cur = lch
                lch = cur * 2 + 1
                rch = cur * 2 + 2
            else:
                break

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            if QuickSort(0, data_size - 1) == -1:
                running = False
            Finalize()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            MergeSort_2()
            Finalize()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            data, data_color = MergeSort_1(data, data_color)
            Finalize()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            HeapSort()
            Finalize()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            DataGenerator()

    Visualize()
