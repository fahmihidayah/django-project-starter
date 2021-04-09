from .models import Profile, UserModel


class ProfileRepository:

    def get_user_profile(self, user : UserModel) -> Profile:
        try:

            return user.profile

        except:
            profile = Profile.objects.create(user=user)
            return profile