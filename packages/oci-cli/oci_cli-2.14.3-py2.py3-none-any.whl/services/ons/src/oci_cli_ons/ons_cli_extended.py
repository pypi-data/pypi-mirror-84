# coding: utf-8
# Copyright (c) 2016, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

import click
from services.ons.src.oci_cli_notification_control_plane.generated import notificationcontrolplane_cli
from services.ons.src.oci_cli_notification_data_plane.generated import notificationdataplane_cli
from .generated import ons_service_cli
from oci_cli.aliasing import CommandGroupWithAlias
from oci_cli import cli_util
from oci_cli import json_skeleton_utils


# Original commands as generated by code-gen
# oci ons notification-control-plane notification-topic create-topic
# oci ons notification-control-plane notification-topic get-topic
# oci ons notification-control-plane notification-topic list-topics
# oci ons notification-control-plane notification-topic update-topic
# oci ons notification-control-plane topic delete
# oci ons notification-data-plane publish-result publish-message
# oci ons notification-data-plane string get-confirm-subscription
# oci ons notification-data-plane string get-unsubscription
# oci ons notification-data-plane subscription create
# oci ons notification-data-plane subscription delete
# oci ons notification-data-plane subscription get
# oci ons notification-data-plane subscription list
# oci ons notification-data-plane subscription-confirmation resend
# oci ons notification-data-plane update-subscription-details update-subscription

# New commands after manual CLI changes
# oci ons topic create
# oci ons topic get
# oci ons topic list
# oci ons topic update
# oci ons topic delete
# oci ons message publish
# oci ons subscription create
# oci ons subscription delete
# oci ons subscription get
# oci ons subscription list
# oci ons subscription update
# oci ons subscription confirm
# oci ons subscription unsubscribe
# oci ons subscription resend-confirmation


# Add a message model group which will be used to add a layer to publish message to a topic operation
@click.command(cli_util.override('message_group.command_name', 'message'), cls=CommandGroupWithAlias, help="""A message for a topic.""")
@cli_util.help_option_group
def message_group():
    pass


# Re-work notification control plane commands
notificationcontrolplane_cli.notification_topic_group.add_command(notificationcontrolplane_cli.delete_topic)
cli_util.rename_command(notificationcontrolplane_cli, ons_service_cli.ons_service_group, notificationcontrolplane_cli.notification_topic_group, "topic")
cli_util.rename_command(notificationcontrolplane_cli, notificationcontrolplane_cli.notification_topic_group, notificationcontrolplane_cli.delete_topic, "delete")
ons_service_cli.ons_service_group.commands.pop(notificationcontrolplane_cli.notification_control_plane_root_group.name)

# Re-work notification data plane commands
cli_util.rename_command(notificationdataplane_cli, notificationdataplane_cli.subscription_group, notificationdataplane_cli.update_subscription, "update")
cli_util.rename_command(notificationdataplane_cli, notificationdataplane_cli.subscription_group, notificationdataplane_cli.get_confirm_subscription, "confirm")
cli_util.rename_command(notificationdataplane_cli, notificationdataplane_cli.subscription_group, notificationdataplane_cli.get_unsubscription, "unsubscribe")
cli_util.rename_command(notificationdataplane_cli, notificationdataplane_cli.subscription_group, notificationdataplane_cli.resend_subscription_confirmation, "resend-confirmation")
ons_service_cli.ons_service_group.add_command(notificationdataplane_cli.subscription_group)
ons_service_cli.ons_service_group.add_command(message_group)
cli_util.rename_command(notificationdataplane_cli, message_group, notificationdataplane_cli.publish_message, "publish")
ons_service_cli.ons_service_group.commands.pop(notificationdataplane_cli.notification_data_plane_root_group.name)

cli_util.rename_command(notificationcontrolplane_cli, notificationcontrolplane_cli.notification_topic_group, notificationcontrolplane_cli.create_topic, "create")
cli_util.rename_command(notificationcontrolplane_cli, notificationcontrolplane_cli.notification_topic_group, notificationcontrolplane_cli.get_topic, "get")
cli_util.rename_command(notificationcontrolplane_cli, notificationcontrolplane_cli.notification_topic_group, notificationcontrolplane_cli.list_topics, "list")
cli_util.rename_command(notificationcontrolplane_cli, notificationcontrolplane_cli.notification_topic_group, notificationcontrolplane_cli.update_topic, "update")


# Rename the endpoint parameter to --subscription-endpoint since it conflicts with the --endpoint parameter that CLI
# provides for all its commands
@cli_util.copy_params_from_generated_command(notificationdataplane_cli.create_subscription, params_to_exclude=['endpoint_parameterconflict'])
@notificationdataplane_cli.subscription_group.command(name=cli_util.override('create_subscription.command_name', 'create'), help=notificationdataplane_cli.create_subscription.help)
@cli_util.option('--subscription-endpoint', required=True, help="""The endpoint of the subscription. Valid values depend on the protocol. For EMAIL, only an email address is valid. For HTTPS, only a PagerDuty URL is valid. A URL cannot exceed 512 characters. Avoid entering confidential information.""")
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'freeform-tags': {'module': 'ons', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'ons', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'ons', 'class': 'Subscription'})
@cli_util.wrap_exceptions
def create_subscription(ctx, subscription_endpoint, **kwargs):
    kwargs['endpoint_parameterconflict'] = subscription_endpoint
    ctx.invoke(notificationdataplane_cli.create_subscription, **kwargs)
