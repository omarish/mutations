import mutations


class SimpleMutation(mutations.Mutation):
    name = mutations.fields.CharField()
    email = mutations.fields.CharField()
    location = mutations.fields.CharField(required=False)