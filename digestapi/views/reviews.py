from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from digestapi.models import Reviews


class ReviewSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Reviews
        fields = ["id", "book", "user", "rating", "comment", "date", "is_owner"]
        read_only_fields = ["user"]

    def get_is_owner(self, obj):
        # Check if the user is the owner of the review
        return self.context["request"].user == obj.user


class ReviewViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        # Get all reviews
        reviews = Reviews.objects.all()
        # Serialize the objects, and pass request to determine owner
        serializer = ReviewSerializer(reviews, many=True, context={"request": request})
        # Return the serialized data with 200 status code
        return Response(serializer.data)

    def create(self, request):
        # Create a new instance of a review and assign property
        # values from the request payload using `request.data`
        rating = request.data("rating")
        comment = request.data("comment")
        date = request.data("date")
        # Save the review
        review = Reviews.objects.create(
            user=request.user, rating=rating, comment=comment, date=date
        )
        try:
            review.save()
            # Serialize the objects, and pass request as context
            serializer = ReviewSerializer(review, context={"request": request})
            # Return the serialized data with 201 status code
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            # Get the requested review
            review = Reviews.objects.get(pk=pk)
            # Serialize the object (make sure to pass the request as context)
            serializer = ReviewSerializer(review, context={"request": request})
            # Return the review with 200 status code
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Reviews.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            # Get the requested review
            review = Reviews.objects.get(pk=pk)
            # Check if the user has permission to delete
            # Will return 403 if authenticated user is not author
            if review.user.id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            # Delete the review
            review.delete()

            # Return success but no body
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Reviews.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
