from django.shortcuts import get_object_or_404
from rest_framework import views, permissions, response, status

from recipes.models import (
    Recipe, Favourite, Purchase, Ingredient, Following, User
)


class AddRemoveMixin:
    model = None
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        pk = request.data.get('id')
        if pk:
            recipe = get_object_or_404(Recipe, pk=int(pk))
            instance = self.model.objects.create(
                user=request.user, recipe=recipe
            )
            success = instance.save()
            return response.Response(
                {'success': bool(success)}, status=status.HTTP_200_OK
            )
        return response.Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        instance = get_object_or_404(
            self.model, user=request.user, recipe__pk=id
        )
        success = instance.delete()
        return response.Response(
            {'success': bool(success)}, status=status.HTTP_200_OK
        )


class Favorites(views.APIView, AddRemoveMixin):
    permission_classes = [permissions.IsAuthenticated]
    model = Favourite


class Purchases(views.APIView, AddRemoveMixin):
    permission_classes = [permissions.IsAuthenticated]
    model = Purchase


class Subscriptions(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        pk = request.data.get('id')
        if pk:
            user = get_object_or_404(User, pk=int(pk))
            if request.user == user:
                return response.Response(
                    status=status.HTTP_405_METHOD_NOT_ALLOWED
                )
            follow = Following.objects.create(user=user, follower=request.user)
            success = follow.save()
            return response.Response(
                {'success': bool(success)}, status=status.HTTP_200_OK
            )

    def delete(self, request, id):
        follow = get_object_or_404(
            Following, user__pk=id, follower=request.user
        )
        success = follow.delete()
        return response.Response(
            {'success': bool(success)}, status=status.HTTP_200_OK
        )


class RecipeCreation(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        text = request.query_params.get('query').lower()
        ingredients = Ingredient.objects.filter(name__startswith=text)
        if ingredients.count() == 0:
            ingredients = Ingredient.objects.filter(name__contains=text)
        queryset = []
        for ingredient in ingredients:
            queryset.append({
                'title': ingredient.name,
                'dimension': ingredient.measurement
            })
        return response.Response(queryset)
