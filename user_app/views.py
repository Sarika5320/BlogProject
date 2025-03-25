from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from admin_app.models import HeroVideo
from .models import BlogPost, Comment
from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from .forms import BlogPostForm,CommentForm,ReplyForm
from django.http import JsonResponse

# Home Page
def home(request):
    videos = HeroVideo.objects.all()  # Fetch all hero videos
    blogs = BlogPost.objects.all().order_by("-created_at")  # Fetch latest blogs

    return render(request, 'user_app/home.html', {'videos': videos, 'blogs': blogs})  # Loads home.html



#User Dashboard
@login_required
def user_dashboard(request):
    user_blogs = BlogPost.objects.filter(user=request.user).order_by("-created_at")  # Fetch only current user's blogs
    return render(request, "user_app/user_dashboard.html", {"blogs": user_blogs})

#Update Profile
@login_required
def update_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        # Update user details
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get("email", user.email)
        profile.bio = request.POST.get("bio", profile.bio)
        profile.phone = request.POST.get("phone", profile.phone)

        # ✅ Fix: Check if a new profile picture is uploaded
        if "profile_picture" in request.FILES:
            new_picture = request.FILES["profile_picture"]

            # ✅ Delete old profile picture before saving a new one
            if profile.profile_picture and profile.profile_picture.name != "profile_pics/default.jpg":
                profile.profile_picture.delete(save=False)

            profile.profile_picture = new_picture

        # ✅ Save changes
        user.save()
        profile.save()

        # ✅ Add success message
        messages.success(request, "Profile updated successfully!")
        return redirect("user_app:settings")

    return render(request, "user_app/settings.html", {"user": user, "profile": profile})

#Create Blog Post
@login_required
def create_blog(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user  # Assign logged-in user as author
            blog.save()
            messages.success(request, "Blog created successfully!")
            return redirect("user_app:user_dashboard")  # Redirect to home after creation
    else:
        form = BlogPostForm()

    return render(request, "user_app/create_blog.html", {"form": form})


#blog detail
def blog_detail(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    comments = blog.comments.filter(parent__isnull=True).order_by('-created_at') # type: ignore
    form = CommentForm()
    reply_form = ReplyForm()

    # Store the source in session (admin or user)
    if 'source' in request.GET:
        request.session['source'] = request.GET['source']
    
    source = request.session.get('source', 'user')  # Default is user if not set

    if request.method == "POST":
        if "comment_id" in request.POST:  # Handling replies
            parent_comment = get_object_or_404(Comment, id=request.POST.get("comment_id"))
            form = ReplyForm(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.user = request.user
                reply.blog = blog
                reply.parent = parent_comment
                reply.save()
                return redirect('user_app:blog_detail', blog.id) # type: ignore
        else:  # Handling new comments
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.blog = blog
                comment.save()
                return redirect('user_app:blog_detail', blog.id) # type: ignore

    return render(request, 'user_app/blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'form': form,
        'reply_form': reply_form,
        'source': source,  # Pass the source to the template
    })


#edit blog
@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id, user=request.user)  # Ensure user owns the blog
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated successfully!")
            #return redirect("user_app:blog_detail", blog_id=blog.id)
            return redirect("user_app:user_dashboard")
    else:
        form = BlogPostForm(instance=blog)
    
    return render(request, "user_app/edit_blog.html", {"form": form, "blog": blog})

#delete blog
@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id, user=request.user)  # Ensure user owns the blog
    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog deleted successfully!")
        return redirect("user_app:user_dashboard")

    return render(request, "user_app/delete_blog.html", {"blog": blog})

#Post a Comment
@login_required
def post_comment(request, blog_id):
    try:
        blog = BlogPost.objects.get(id=blog_id)
        if request.method == "POST":
            Comment.objects.create(user=request.user, blog=blog, content=request.POST.get("content", ""))
            messages.success(request, "Comment added!")
    except BlogPost.DoesNotExist:
        messages.error(request, "Blog post not found.")
    return redirect("blog_detail", blog_id=blog_id)

def like_post(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    
    if request.user.is_authenticated:
        if blog.likes.filter(id=request.user.id).exists():
            blog.likes.remove(request.user)  # Unlike if already liked
            liked = False
        else:
            blog.likes.add(request.user)  # Like the post
            liked = True

        return JsonResponse({"liked": liked, "total_likes": blog.total_likes()})  # Return JSON response

    return redirect('accounts:login')  # Redirect if user is not logged in
