from member_organisations.models import MemberOrganisationOwner, MemberOrganisation


def get_allowed_mo_for_mo_admin(user):
    if user.is_superuser:
        return MemberOrganisation.objects.all()

    member_organization_admin_ids = (  # mo where the current user is admin
        user.member_organisations_memberorganisationuser
        .filter(is_admin=True)
        .values_list('organization', flat=True)
    )
    member_organization_owner_ids = (  # mo where the current user is owner
        MemberOrganisationOwner.objects
            .filter(organization__owner__organization_user__user=user)
            .values_list('organization', flat=True)
    )

    allowed_organizations = (
            set(member_organization_admin_ids) | set(member_organization_owner_ids)
    )

    return allowed_organizations
