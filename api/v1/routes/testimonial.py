#!/usr/bin/env python3
"""
Module contains CRUD routes for testimonial
"""
from api.db.database import get_db
from sqlalchemy.orm import Session
from api.utils.dependencies import get_super_admin
from api.v1.models.user import User
from api.v1.models.testimonial import Testimonial
from uuid import UUID
from fastapi import Depends, HTTPException, APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from api.utils.success_response import success_response
from api.v1.services.testimonial import testimonial_service
from api.v1.services.user import user_service

testmonial_route = APIRouter(prefix='/testimonials', tags=['Testimonial'])

@testmonial_route.delete("/{testimonial_id}")
def delete_testimonial(
    testimonial_id: UUID,
    current_user: User = Depends(get_super_admin),
    db: Session = Depends(get_db)
):
    """
    Function for deleting a testimonial based on testimonial id
    """
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(
            detail="Testimonial not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    db.delete(testimonial)
    db.commit()
    return JSONResponse(
        content={
            "success": True,
            "message": "Testimonial deleted successfully",
            "status_code": status.HTTP_200_OK
        },
        status_code=status.HTTP_200_OK
    )

      
@testmonial_route.get('/{testimonial_id}', status_code=status.HTTP_200_OK)
def get_testimonial(testimonial_id, db: Session = Depends(get_db), current_user: User = Depends(user_service.get_current_user)):
    '''Endpoint to get testimonial by id'''

    testimonial = testimonial_service.fetch(db, testimonial_id)
    if testimonial and testimonial_id == testimonial.id:
        return success_response(
            status_code=200,
            message=f'Testimonial {testimonial_id} retrieved successfully',
            data={
                'id': testimonial.id,
                'client_designation': testimonial.client_designation,
                'client_name': testimonial.client_name,
                'author_id': testimonial.author_id,
                'comments': testimonial.comments,
                'content': testimonial.content,
                'ratings': testimonial.ratings, 
            }
        )
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "status_code": 404,
            "message": f'Testimonial {testimonial_id} not found'
        }
    )
