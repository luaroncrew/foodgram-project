from rest_framework import views, permissions, response, status

from recipes.models import Recipe, Favourite, Purchase, Ingredient, Following, User


# мне нужна подсказка, как можно эти две вьюхи снизу оптимизировать.
# у них только в модели отличия
class Favorites(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        pk = int(request.data.get('id'))
        recipe = Recipe.objects.get(pk=pk)
        favourite = Favourite.objects.create(user=request.user, recipe=recipe)
        success = favourite.save()
        return response.Response({'success': bool(success)}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        recipe = Recipe.objects.get(pk=id)
        favourite = Favourite.objects.get(user=request.user, recipe=recipe)
        success = favourite.delete()
        return response.Response({'success': bool(success)}, status=status.HTTP_200_OK)


class Purchases(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        pk = int(request.data.get('id'))
        recipe = Recipe.objects.get(pk=pk)
        purchase = Purchase.objects.create(user=request.user, recipe=recipe)
        success = purchase.save()
        return response.Response({'success': bool(success)}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        recipe = Recipe.objects.get(pk=id)
        favourite = Purchase.objects.get(user=request.user, recipe=recipe)
        success = favourite.delete()
        return response.Response({'success': bool(success)}, status=status.HTTP_200_OK)


class Subscriptions(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        pk = int(request.data.get('id'))
        user = User.objects.get(pk=pk)
        if request.user == user:
            return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        follow = Following.objects.create(user=user, follower=request.user)
        success = follow.save()
        return response.Response({'success': bool(success)}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        follow = Following.objects.get(user__pk=id, follower=request.user)
        success = follow.delete()
        return response.Response({'success': bool(success)}, status=status.HTTP_200_OK)


class RecipeCreation(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        text = request.query_params.get('query').lower()
        if text:
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
