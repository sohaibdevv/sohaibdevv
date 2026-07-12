type HealthResponse = {
  status: "ok";
  service: string;
};

export async function health(): Promise<HealthResponse> {
  return { status: "ok", service: "agentsphere-x-dev-api" };
}

