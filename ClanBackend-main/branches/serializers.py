from rest_framework import serializers

from branches.models import Branch


class BranchSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Branch
        fields = '__all__'
