from onto import domain_model, attrs


class LocationBase(domain_model.DomainModel):

    class Meta:
        collection_name = "locations"

    latitude = attrs.bproperty()
    longitude = attrs.bproperty()
    address = attrs.bproperty()


class Location(LocationBase):

    pass
