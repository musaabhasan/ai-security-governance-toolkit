package ai.agent

default allow := false

high_impact_actions := {
  "delete_record",
  "send_external_email",
  "change_access",
  "approve_request",
  "execute_code",
}

allow if {
  input.agent.approved == true
  input.tool.name in input.agent.allowed_tools
  not high_impact_actions[input.action]
  input.data_classification != "regulated"
}

allow if {
  input.agent.approved == true
  input.tool.name in input.agent.allowed_tools
  high_impact_actions[input.action]
  input.human_approval.approved == true
  input.human_approval.approver != input.agent.id
}

deny_reason contains "agent is not approved" if {
  input.agent.approved != true
}

deny_reason contains "tool is not allowlisted" if {
  not input.tool.name in input.agent.allowed_tools
}

deny_reason contains "regulated data requires explicit human approval" if {
  input.data_classification == "regulated"
  input.human_approval.approved != true
}

deny_reason contains "high-impact action requires independent approval" if {
  high_impact_actions[input.action]
  input.human_approval.approved != true
}
