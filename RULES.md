# Rule Documentation

The following serves to document the possible arguments that each of our rules
takes, to ease users in generating config files.

## `IPRangeRule`

- `action`: Chain to send the packet to if it matches.
- `cidr_range`: The IP address range to match on, specified in CIDR (Classless Inter-Domain Routing) format.

### `SourceIPRule` and `DestinationIPRule`

Both derive from `IPRangeRule`, so their arguments are the same.

## `PortRule`

- `action`: Chain to send the packet to if it matches.
- `protocol`: Which protocol to match on. 'TCP' or 'UDP'.
- `src_port`: Which source port to match on.
- `dst_port`: Which destination port to match on.

Only one of `src_port` and `dst_port` is required for the rule to function.

## `PortRangeRule`

- `action`: Chain to send the packet to if it matches.
- `protocol`: Which protocol to match on. 'TCP' or 'UDP'.
- `src_lo`: Lower bound of the source port range. Inclusive.
- `src_hi`: Upper bound of the source port range. Inclusive.
- `dst_lo`: Lower bound of the destination port range. Inclusive.
- `dst_hi`: Upper bound of the destination port range. Inclusive.

Either a source port range or destination port range must be specified, though
you can use both in conjunction.

## `IPPortRule`

This rule is a composition of the `IPRangeRule` and `PortRangeRule` so most of
its arguments are derived from there. Note:

- `src_ip`: The CIDR range to match on source addresses.
- `dst_ip`: The CIDR range to match on destination addresses.

Only one of `src_ip` and `dst_ip` is required.

## `TCPRule`

- `action`

## `TCPStateRule`

- `action`
- `match_if`: A set of TCP states. The rule will match on packets whose TCP state is in this set.
- `match_if_not`: A set of TCP states. The rule will match on packets whose TCP state is not in this set.

You may only specify one of `match_if` and `match_if_not`. They cannot be used
in conjunction.

## `PortKnocking`

- `protocol`: Which protocol to match on. 'TCP' or 'UDP'.
- `src_port`: Source port that ultimately will be connected to, upon successful knocking.
- `timeout`: How long the rule should maintain state about a knocking attempt.
- `doors`: Doors to knock on. A list of (protocol, port) tuples.

## Example Configuration

```
{
  "default_chain": "ACCEPT",
  "INPUT":[
    {"name":"PrintRule"},
    {"name":"PortKnocking",
     "src_port": 9001,
     "protocol": "TCP",
     "port": 2222,
     "timeout": 20,
     "doors": [["TCP", 49001], ["UDP", 49011]]},
    {"name":"TCPStateRule",
     "match_if": ["CLOSED"],
     "action": "DROP"},
    {"name":"SourceIPRule",
     "action": "DROP",
     "cidr_range": "221.224.0.0/13"}
   ]
}
```
