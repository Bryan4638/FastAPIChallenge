from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from modules.comment.dto.request_comment_dto import RequestCommentDTO
from modules.comment.dto.response_comment import ResponseCommentDTO
from modules.comment.use_cases.create_comment import CreateComment
from modules.comment.use_cases.delete_comment import DeleteComment
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

    comment = await UpdateComment.update_comment(db, comment_id, user_id, update_data)

    if not comment:
        raise ValueError("Comment not found")

    return ResponseCommentDTO(
        id=comment.id,
        content=comment.content,
        post_id=comment.post_id,
        author_id=comment.author_id,
        created_at=comment.created_at
    )

async def delete_comment_service(
    db: AsyncSession,
    comment_id: UUID,
    user_id: UUID
) -> bool:

    is_delete = await DeleteComment.delete_comment(db, user_id, comment_id)

    if not is_delete:
        raise ValueError("Comment not found")

    return is_delete
