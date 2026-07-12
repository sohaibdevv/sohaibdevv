import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const body = (await req.json()) as { message?: string };
  return NextResponse.json({
    ok: true,
    echo: body.message ?? "",
    runtime: "mastra-bridge",
  });
}

