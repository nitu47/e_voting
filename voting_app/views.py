import random
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Voter, Candidate
from .forms import RegisterForm, OTPForm

# -------------------
# HELPER FUNCTIONS
# -------------------

def generate_otp():
    """Generate a random 6-digit OTP"""
    return str(random.randint(100000, 999999))


# -------------------
# MAIN VIEWS
# -------------------

def home(request):
    return render(request, 'voting_app/home.html')


# -------------------
# REGISTER VIEW (Only pre-registered voters can vote)
# -------------------
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email'].lower()

            # Check if email is pre-registered
            try:
                voter = Voter.objects.get(email=email)
            except Voter.DoesNotExist:
                messages.error(request, 'This Gmail is not registered for voting.')
                return redirect('voting_app:register')

            # Check if voter already voted
            if voter.has_voted:
                messages.error(request, 'You have already voted.')
                return redirect('voting_app:register')

            # Update name if needed
            if voter.name != name:
                voter.name = name
                voter.save()

            # Generate OTP
            otp = generate_otp()
            voter.otp = otp
            voter.is_verified = False
            voter.save()

            # Send email
            send_mail(
                subject='Your OTP for E-Voting',
                message=f'Hello {voter.name},\n\nYour OTP for voting is: {otp}\n\nDo not share it with anyone.',
                from_email=getattr(settings, 'EMAIL_FROM', settings.EMAIL_HOST_USER),
                recipient_list=[voter.email],
            )

            request.session['voter_email'] = voter.email
            messages.success(request, 'OTP sent to your registered Gmail.')
            return redirect('voting_app:verify_otp')

    else:
        form = RegisterForm()

    return render(request, 'voting_app/register.html', {'form': form})


# -------------------
# OTP VERIFICATION
# -------------------
def verify_otp(request):
    voter_email = request.session.get('voter_email')
    if not voter_email:
        messages.error(request, 'No registration in progress. Please register first.')
        return redirect('voting_app:register')

    voter = get_object_or_404(Voter, email=voter_email)

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp'].strip()

            if voter.otp == otp:
                voter.is_verified = True
                voter.otp = ''
                voter.save()
                messages.success(request, 'OTP verified. You can now vote.')
                return redirect('voting_app:vote_list')
            else:
                messages.error(request, 'Invalid OTP. Try again.')

    else:
        form = OTPForm()

    return render(request, 'voting_app/verify_otp.html', {'form': form, 'voter': voter})


# -------------------
# SHOW CANDIDATE LIST
# -------------------
def vote_list(request):
    voter_email = request.session.get('voter_email')

    if not voter_email:
        messages.error(request, 'Please register and verify before voting.')
        return redirect('voting_app:register')

    voter = get_object_or_404(Voter, email=voter_email)

    if not voter.is_verified:
        messages.error(request, 'Please verify OTP before voting.')
        return redirect('voting_app:verify_otp')

    # No IP/device restriction — ONLY one vote per registered voter
    candidates = Candidate.objects.all()
    return render(request, 'voting_app/vote_list.html', {'candidates': candidates, 'voter': voter})


# -------------------
# VOTE FOR A CANDIDATE
# -------------------
def vote_candidate(request, candidate_id):
    voter_email = request.session.get('voter_email')

    if not voter_email:
        messages.error(request, 'Please register and verify before voting.')
        return redirect('voting_app:register')

    voter = get_object_or_404(Voter, email=voter_email)

    if not voter.is_verified:
        messages.error(request, 'Please verify OTP before voting.')
        return redirect('voting_app:verify_otp')

    if voter.has_voted:
        messages.error(request, 'You have already voted.')
        return redirect('voting_app:results')

    # Count vote
    candidate = get_object_or_404(Candidate, id=candidate_id)
    candidate.votes += 1
    candidate.save()

    # Mark voter as voted
    voter.has_voted = True
    voter.save()

    messages.success(request, f'Thank you for voting for {candidate.name}!')
    return redirect('voting_app:results')


# -------------------
# RESULTS PAGE
# -------------------
def results(request):
    candidates = Candidate.objects.all().order_by('-votes')
    total_votes = sum(c.votes for c in candidates)

    names = [c.name for c in candidates]
    votes = [c.votes for c in candidates]

    return render(request, 'voting_app/results.html', {
        'candidates': candidates,
        'total_votes': total_votes,
        'names': names,
        'votes': votes,
    })


# -------------------
# LOGOUT
# -------------------
def user_logout(request):
    request.session.flush()
    messages.info(request, 'Session cleared.')
    return redirect('voting_app:home')
