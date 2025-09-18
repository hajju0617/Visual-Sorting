import os
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from math import ceil, floor

pygame.init()
# 프로그램 제목
pygame.display.set_caption("Sorting Visualization")
# 화면의 크기 (가로, 세로)
screensize = (640, 580)
screen = pygame.display.set_mode(screensize)
clock = pygame.time.Clock()
framerate = 10
running = True

font = pygame.font.Font(None, 30)
# 텍스트를 줄 단위로 분리 (상단에 표시할 설명)
text_lines = [
    "Sorting Visualization",
    "",
    "*q: Quick Sorting [ O(nlogn) ]",
    "*m: Merge Sorting [ O(nlogn) ]",
    "*h: Heap Sorting [ O(nlogn) ]",
    "",
    "*g: Random Data Generation"
]

# 정렬할 & 시각화할 데이터의 개수.
data_size = 64
# 정렬할 데이터들을 저장하는 리스트. (막대 그래프 높이로 사용)
data = list()
# 각 데이터에 해당하는 색상을 저장하는 리스트.
data_color = list()

# 무작위 데이터를 생성하는 함수.
def DataGenerator():
    global data
    global data_color
    # data_size 만큼 10에서 400 사이의 무작위 데이터를 생성. (막대 그래프 높이로 사용)
    data = [random.randint(10, 400) for i in range(data_size)]
    # data_size 만큼 무작위 RGB 색상 값(튜플 형태)을 생성.
    data_color = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
                  for i in range(data_size)]
# 프로그램 시작 시 최초 데이터(높이/색상)를 생성.
DataGenerator()

# data 리스트를 화면에 그리는 함수.
def Visualize():
    screen.fill("black")
    
    # 텍스트를 적기 시작할 Y 좌표.
    start_y = 20  
    line_height = font.get_linesize()  # 폰트 한 줄의 높이.
    for i, line in enumerate(text_lines):
        text_surface = font.render(line, True, "gray")
        text_rect = text_surface.get_rect()
        text_rect.center = (screen.get_width() / 2, start_y + i * line_height)
        screen.blit(text_surface, text_rect)

    # 데이터(막대 그래프) 출력.
    for i in range(data_size):
        pygame.draw.rect(screen, data_color[i], (i*10, screensize[1]-data[i], 10, data[i]))
    # 화면에 그린 내용을 실제 화면에 업데이트하여 출력.
    pygame.display.flip()
    clock.tick(framerate)

# 정렬이 완료되었음을 알리는 함수.
def Finalize():
    screen.fill("white")
    pygame.display.flip()
    clock.tick(framerate)

# 실행도중 사용자의 입력을 처리하는 함수.
def EventHandler():
    for event in pygame.event.get():
        # ESC 누름 -> 중단.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return -1
        # 창 닫기 버튼 -> 프로그램 종료.
        elif event.type == pygame.QUIT:
            exit()

# 퀵 정렬.
def QuickSort(start, end):
    if start >= end:
        return
    # 피벗을 start로 선택.
    pivot = start
    left = start + 1
    right = end

    while left <= right:
        if EventHandler() == -1:
            return

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
        # 데이터 위치가 바뀔 때마다 Visualize()를 호출하여 현재 상태를 화면에 출력.
        Visualize()

    QuickSort(start, right-1)
    QuickSort(right+1, end)

# 합병 정렬 (시각화 X)
def MergeSort_1(data_list, color_list):
    if len(data_list) < 2:
        return data_list, color_list
    # 중간 인덱스.
    mid = len(data_list) // 2
    # 리스트를 반으로 나눠 low와 high 부분으로 재귀 호출. (왼쪽:low, 오른쪽:high)
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

# 합병 정렬 (시각화 O)
def MergeSort_2():
    # 재귀호출로 데이터를 나누는 역할.
    def sort(low, high):
        if EventHandler() == -1:
            return

        if high - low < 2:
            return
    # 중간 인덱스 계산 후 좌우를 재귀호출로 정렬하고 merge로 병합.
        mid = (low + high) // 2
        sort(low, mid)
        sort(mid, high)
        merge(low, mid, high)
    # 나뉜 두 부분을 합병.
    def merge(low, mid, high):
        data_temp = list()
        color_temp = list()
        # l(왼쪽 시작), h(오른쪽 시작)
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

    sort(0, data_size)
# 힙 정렬
def HeapSort():
    for i in range(len(data)):
        # i : 현재 노드 인덱스, par : 부모 노드 인덱스
        par = floor((i - 1) / 2)
        while par >= 0 and data[par] < data[i]:
            data[par], data[i] = data[i], data[par]
            data_color[par], data_color[i] = data_color[i], data_color[par]
            i = par
            par = floor((i - 1) / 2)

    for i in range(len(data)-1, 0, -1):
        data[0], data[i] = data[i], data[0]
        data_color[0], data_color[i] = data_color[i], data_color[0]
        # cur : 현재 노드 인덱스, lch : 왼쪽 자식 인덱스, rch : 오른쪽 자식 인덱스
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
                lch = i  # break와 같은 효과

            if not lch < i:
                break
# running 변수가 True인 동안 무한 반복.
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            QuickSort(0, data_size - 1)
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
    # 실행 후 항상 Visualize()를 호출하여 현재 상태를 화면에 출력.
    Visualize()