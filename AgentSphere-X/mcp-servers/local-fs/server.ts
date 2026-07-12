type ToolRequest = {
  tool: "read_tree";
  root: string;
};

export function handleTool(req: ToolRequest) {
  return {
    tool: req.tool,
    root: req.root,
    mode: "safe-readonly",
  };
}

