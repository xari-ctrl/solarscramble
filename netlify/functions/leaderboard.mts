import type { Config } from "@netlify/functions";
import { desc } from "drizzle-orm";
import { db } from "../../db/index.js";
import { leaderboardScores } from "../../db/schema.js";

export default async (req: Request) => {
  if (req.method === "GET") {
    const top = await db
      .select({ name: leaderboardScores.name, score: leaderboardScores.score })
      .from(leaderboardScores)
      .orderBy(desc(leaderboardScores.score))
      .limit(10);
    return Response.json(top);
  }

  if (req.method === "POST") {
    const body = await req.json().catch(() => null);
    const name = typeof body?.name === "string" ? body.name.trim().slice(0, 18) || "Astronaut" : "Astronaut";
    const score = Number(body?.score);

    if (!Number.isFinite(score) || score < 0) {
      return new Response("Invalid score", { status: 400 });
    }

    await db.insert(leaderboardScores).values({ name, score: Math.round(score) });

    const top = await db
      .select({ name: leaderboardScores.name, score: leaderboardScores.score })
      .from(leaderboardScores)
      .orderBy(desc(leaderboardScores.score))
      .limit(10);
    return Response.json(top, { status: 201 });
  }

  return new Response("Method not allowed", { status: 405 });
};

export const config: Config = {
  path: "/api/leaderboard",
};
