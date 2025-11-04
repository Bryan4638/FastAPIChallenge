from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from modules.comment.dto.request_comment_dto import RequestCommentDTO
from modules.comment.dto.response_comment import ResponseCommentDTO
from modules.comment.use_cases.create_comment import CreateComment
from modules.comment.use_cases.delete_comment import DeleteComment
from modules.comment.use_cases.find_by_id import FindCommentById
from modules.comment.use_cases.update_comment import UpdateComment


async def create_comment_service(
        db: AsyncSession,
        comment_data: RequestCommentDTO,
        user_id: str
) -> Optional[ResponseCommentDTO]:

    comment = await CreateComment.create_comment(db, comment_data, user_id)

    return ResponseCommentDTO(
        id=comment.id,
        content=comment.content,
        post_id=comment.post_id,
        author_id=comment.author_id,
        created_at=comment.created_at
    )


async def update_comment_service(
    db: AsyncSession,
    comment_id: UUID,
    user_id: UUID,
    update_data: RequestCommentDTO
) -> Optional[ResponseCommentDTO]:

    comment = await FindCommentById.find_by_id(db, comment_id)

    if not comment:
        return None

    if str(user_id) != str(comment.author_id):
        print("User id ----->", user_id)
        print("Comment author id ----->", comment.author_id)
        raise ValueError(f"User {user_id} is not the author of comment {comment_id}")

    comment_update = await UpdateComment.update_comment(db, comment_id, user_id, comment ,update_data)

    if not comment_update:
        raise ValueError("Comment not found")

    return ResponseCommentDTO(
        id=comment_update.id,
        content=comment_update.content,
        post_id=comment_update.post_id,
        author_id=comment_update.author_id,
        created_at=comment_update.created_at
    )

async def delete_comment_service(
    db: AsyncSession,
    comment_id: UUID,
    user_id: UUID
) -> bool:
    comment = await FindCommentById.find_by_id(db, comment_id)

    if not comment:
        return False

    if str(user_id) != str(comment.author_id):
        raise ValueError(f"User {user_id} is not the author of comment {comment_id}")

    is_delete = await DeleteComment.delete_comment(db, comment)

    if not is_delete:
        raise ValueError("Comment not found")

    return is_delete
