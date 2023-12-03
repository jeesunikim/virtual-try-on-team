from django.http import HttpRequest
from ninja import Query, UploadedFile, File, Router
from try_on.models import Try, User

from try_on.schemas import TryOnRequest

router = Router()


@router.post("/try_on_outfit")
def try_on_outfit(
    request: HttpRequest,
    payload: TryOnRequest,
    selfie: UploadedFile = File(...),
    outfit: UploadedFile = File(...),
):
    # Find the user by email
    user, _ = User.objects.get_or_create(email=payload.email)
    try_on = Try.objects.create(user=user)

    # try_on.save()

    # TODO upload to s3
    try_on.selfie.save(selfie.name, selfie)
    try_on.outfit.save(outfit.name, outfit)

    # send images to mode
    _send_images_to_model()

    # send email to user
    _send_email_to_user()

    # Wait for training
    _poll_training_model()

    # Send response from ML model
    return {"message": "This is what it looks like"}


def _send_images_to_model():
    pass


def _send_email_to_user():
    pass


def _poll_training_model():
    pass
