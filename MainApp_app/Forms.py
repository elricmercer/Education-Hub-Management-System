from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class TimeInput(forms.TimeInput):
    input_type = "time"


# COMMON
class EditProfileForm(forms.Form):
    genderList = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Others", "Others")
    )

    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}),
                               max_length=150)
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}), max_length=254)
    firstName = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'class': 'form-control'}),
                                max_length=150)
    lastName = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'class': 'form-control'}),
                               max_length=150)
    gender = forms.ChoiceField(label="Gender", choices=genderList, widget=forms.Select(attrs={'class': 'form-control'}))
    dob = forms.DateField(label="Date of Birth", widget=DateInput(attrs={'class': 'form-control'}))
    phoneNo = forms.CharField(label="PhoneNo", widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=20)
    profilePic = forms.FileField(label="Profile Picture", required=False,
                                 widget=forms.FileInput(attrs={'class': 'form-control'}))

    def clean(self):
        check = self.cleaned_data
        if check.get('firstName').isalpha():
            pass
        else:
            self.add_error('firstName', "Error! Please enter alphabets only")

        if check.get('lastName').isalpha():
            pass
        else:
            self.add_error('lastName', "Error! Please enter alphabets only")

        if check.get('phoneNo').isnumeric():
            pass
        else:
            self.add_error('phoneNo', "Error! Please correct phone number")
# END OF COMMON


# ADMIN

# END OF ADMIN


# STUDENT

# END OF STUDENT


# TUTOR

# END OF TUTOR
