from django.db import models
from django.contrib.auth.models import User

#po文
class Post (models.Model):
    content = models.TextField('內文')
    #user撰寫文章
    #建立User和Post之間一對多的關係(一個user可以寫多篇文章)
    creator = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                verbose_name='建立者',
                                related_name='posts')   
    #貼文按讚
    #建立User和Post之間多對多的關係(會多一張like表)
    likes = models.ManyToManyField(User, 
                                related_name='liked_posts',
                                blank= True)    #允許貼文沒有人按讚 
    create_at = models.DateTimeField('建立時間', auto_now_add=True)
    update_at = models.DateTimeField('更新時間', auto_now=True)

    def __str__(self):
        return '{}.Post create by {}'.format(
                self.id,
                self.creator.username,)

#留言
class Commit(models.Model):
    post = models.ForeignKey(Post, 
                            on_delete=models.CASCADE,      #ondeletecascade-文章刪除留言也會刪除
                            verbose_name='文章',
                            related_name='commits')    
    content = models.TextField('內文')

    creator = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                verbose_name='建立者',
                                related_name='commits')   

    likes = models.ManyToManyField(User, 
                                related_name='liked_commits',
                                blank= True)    #允許貼文沒有人按讚
    create_at = models.DateTimeField('建立時間', auto_now_add=True)
    update_at = models.DateTimeField('更新時間', auto_now=True)

    def __str__(self):
        return 'Post create by {}'.format(self.creator.username)
