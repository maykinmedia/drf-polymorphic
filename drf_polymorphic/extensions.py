from drf_spectacular.extensions import OpenApiSerializerExtension
from drf_spectacular.plumbing import ResolvedComponent, build_object_type

from .serializers import PolymorphicSerializer


class PolymorphicSerializerExtension(OpenApiSerializerExtension):
    """
    drf-spectacular extension for :class:`PolymorphicSerializer`
    """

    target_class = PolymorphicSerializer
    match_subclasses = True

    def _get_name_base(self) -> str:
        serializer = self.target
        name = serializer.__class__.__name__
        if name.endswith("Serializer"):
            name = name[:-10]
        return name

    def map_serializer(self, auto_schema, direction):
        sub_components = []
        serializer = self.target
        base_name = self._get_name_base()

        # get the base serializer

        main = ResolvedComponent(
            name=f"{base_name}Shared",
            type=ResolvedComponent.SCHEMA,
            schema=auto_schema._map_basic_serializer(serializer, direction),
            object=serializer,
        )
        auto_schema.registry.register(main)

        # build the components for the polymorphic extra fields
        for (
            discriminator_value,
            sub_serializer,
        ) in serializer.serializer_mapping.items():
            resolved = auto_schema.resolve_serializer(sub_serializer, direction)

            if not resolved.name:
                # serializer didn't have any declared properties
                generic = ResolvedComponent(
                    name="GenericObject",
                    type=ResolvedComponent.SCHEMA,
                    object=sub_serializer,
                )
                generic.schema = build_object_type(
                    description="Generic object",
                    # displays 'property name * - any' in ReDoc
                    additionalProperties=True,
                )
                auto_schema.registry.register_on_missing(generic)
                resolved = generic

            combined = ResolvedComponent(
                name=f"{base_name}{resolved.name}",
                type=ResolvedComponent.SCHEMA,
                schema={
                    "allOf": [
                        main.ref,
                        resolved.ref,
                    ]
                },
                object=(serializer, sub_serializer),
            )
            if combined in auto_schema.registry:
                combined = auto_schema.registry[combined]
            else:
                auto_schema.registry.register(combined)
            sub_components.append((discriminator_value, combined.ref))

        refs = [tuple(ref.items()) for _, ref in sub_components]
        unique_refs = list(dict.fromkeys(refs))

        return {
            "oneOf": [dict(ref) for ref in unique_refs],
            "discriminator": {
                "propertyName": serializer.discriminator_field,
                "mapping": {
                    resource_type: ref["$ref"] for resource_type, ref in sub_components
                },
            },
        }
