from rest_framework import permissions
#po文
class IsCreatorOrReadOnly(permissions.BasePermission):

    #確認文章的所有者是與要求更改的user是一樣的
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator == request.user
#留言
# class CanUpdateOrDeleteCommit(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS\
#                 or request.method == 'POST':
#             return True

#         return obj.creator == request.user        