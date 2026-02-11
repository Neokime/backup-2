from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Board
from .forms import BoardCreateForm, BoardUpdateForm




# 글 등록
def create_board(request):
    form = BoardCreateForm()

    if request.method == 'POST':
        form = BoardCreateForm(request.POST)

        if form.is_valid():
            board = form.save(commit=False)
            board.save()
            messages.success(request, "게시글이 등록되었습니다.")
            return redirect("board:list")
        else:
            messages.error(request, "게시글 등록 실패")

    return render(request, "board/create.html", {"form": form})


# 글 목록
def get_boards(request):
    boards = Board.objects.all().order_by("-id")
    return render(request, "board/list.html", {"boards": boards})


# 글 상세보기
def get_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    return render(request, "board/read.html", {"board": board})


# 글 수정 (title, content만 수정)
def update_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    form = BoardUpdateForm(instance=board)

    if request.method == "POST":
        form = BoardUpdateForm(request.POST, instance=board)

        if form.is_valid():
            form.save()
            messages.success(request, "게시글이 수정되었습니다.")
            return redirect("board:read", board_id=board.id)
        else:
            messages.error(request, "게시글 수정 실패")

    return render(request, "board/update.html", {"form": form})


# 글 삭제
def delete_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)

    if request.method == "POST":
        board.delete()
        messages.success(request, "게시글이 삭제되었습니다.")
        return redirect("board:list")

    return redirect("board:read", board_id=board.id)


