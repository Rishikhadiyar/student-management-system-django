from django import forms

from students.models import Course, Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "email", "age", "course", "profile_image"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-300 bg-white/90 px-4 py-3 text-sm font-medium text-slate-800 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100",
                    "placeholder": "Enter full name",
                    "autofocus": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-300 bg-white/90 px-4 py-3 text-sm font-medium text-slate-800 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100",
                    "placeholder": "Enter email address",
                }
            ),
            "age": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-300 bg-white/90 px-4 py-3 text-sm font-medium text-slate-800 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100",
                    "placeholder": "Enter age",
                    "min": 1,
                    "max": 120,
                    "step": 1,
                }
            ),
            "course": forms.Select(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-300 bg-white/90 px-4 py-3 text-sm font-medium text-slate-800 shadow-sm outline-none transition focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100",
                }
            ),
            "profile_image": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*",
                    "class": "w-full rounded-2xl border border-dashed border-slate-300 bg-white/90 px-4 py-3 text-sm font-medium text-slate-700 shadow-sm outline-none transition file:mr-3 file:rounded-xl file:border-0 file:bg-emerald-50 file:px-3 file:py-1.5 file:text-xs file:font-semibold file:text-emerald-700 hover:file:bg-emerald-100 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].required = False
        self.fields["course"].queryset = Course.objects.all().order_by("name")
        self.fields["course"].empty_label = "Select course (optional)"

    def clean_age(self):
        age = self.cleaned_data["age"]
        if age < 1:
            raise forms.ValidationError("Age must be greater than 0.")
        return age
