/**
 * JobGuard AI - Threat Graph Visualizer & Force-Directed Layout Engine
 * Computes graph physics simulation, edge force relaxation, node clustering,
 * and high-performance SVG/Canvas rendering coordinates for scam syndicate topologies.
 */

export interface GraphNode {
  id: string;
  label: string;
  type: 'RECRUITER' | 'DOMAIN' | 'PAYMENT_WALLET' | 'ATS_PORTAL' | 'PHONE' | 'VICTIM';
  riskScore: number; // 0 to 100
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  clusterId?: string;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  relationship: 'COMMUNICATED_VIA' | 'DEMANDED_PAYMENT_TO' | 'HOSTED_ON' | 'IMPERSONATED_BY' | 'CLONED_FROM';
  weight: number;
  isFlaggedFraud: boolean;
}

export interface GraphLayoutConfiguration {
  width: number;
  height: number;
  attractionStrength: number;
  repulsionConstant: number;
  dampingFactor: number;
  gravityCenter: { x: number; y: number };
  maxIterations: number;
}

export class ThreatGraphVisualizer {
  private nodes: Map<string, GraphNode> = new Map();
  private edges: GraphEdge[] = [];
  private config: GraphLayoutConfiguration;

  constructor(config?: Partial<GraphLayoutConfiguration>) {
    this.config = {
      width: 800,
      height: 600,
      attractionStrength: 0.04,
      repulsionConstant: 4500,
      dampingFactor: 0.85,
      gravityCenter: { x: 400, y: 300 },
      maxIterations: 120,
      ...config,
    };
  }

  public addNode(node: Omit<GraphNode, 'vx' | 'vy'>): void {
    this.nodes.set(node.id, {
      ...node,
      vx: 0,
      vy: 0,
    });
  }

  public addEdge(edge: GraphEdge): void {
    this.edges.push(edge);
  }

  public computeLayoutStep(): void {
    const nodeList = Array.from(this.nodes.values());

    // 1. Repulsion forces between all node pairs (Coulomb's Law)
    for (let i = 0; i < nodeList.length; i++) {
      const nodeA = nodeList[i];
      for (let j = i + 1; j < nodeList.length; j++) {
        const nodeB = nodeList[j];
        const dx = nodeB.x - nodeA.x;
        const dy = nodeB.y - nodeA.y;
        const distSq = Math.max(100, dx * dx + dy * dy);
        const dist = Math.sqrt(distSq);

        const force = this.config.repulsionConstant / distSq;
        const fx = (dx / dist) * force;
        const fy = (dy / dist) * force;

        nodeA.vx -= fx;
        nodeA.vy -= fy;
        nodeB.vx += fx;
        nodeB.vy += fy;
      }
    }

    // 2. Spring attraction forces along connected edges (Hooke's Law)
    for (const edge of this.edges) {
      const source = this.nodes.get(edge.source);
      const target = this.nodes.get(edge.target);
      if (!source || !target) continue;

      const dx = target.x - source.x;
      const dy = target.y - source.y;
      const dist = Math.max(1, Math.sqrt(dx * dx + dy * dy));

      const springForce = (dist - 120) * this.config.attractionStrength * edge.weight;
      const fx = (dx / dist) * springForce;
      const fy = (dy / dist) * springForce;

      source.vx += fx;
      source.vy += fy;
      target.vx -= fx;
      target.vy -= fy;
    }

    // 3. Central gravitational pull
    for (const node of nodeList) {
      const dx = this.config.gravityCenter.x - node.x;
      const dy = this.config.gravityCenter.y - node.y;
      node.vx += dx * 0.005;
      node.vy += dy * 0.005;

      // Update positions with damping
      node.x += node.vx * this.config.dampingFactor;
      node.y += node.vy * this.config.dampingFactor;

      // Bound within canvas
      node.x = Math.max(node.radius, Math.min(this.config.width - node.radius, node.x));
      node.y = Math.max(node.radius, Math.min(this.config.height - node.radius, node.y));
    }
  }

  public runCompleteLayout(): GraphNode[] {
    for (let i = 0; i < this.config.maxIterations; i++) {
      this.computeLayoutStep();
    }
    return Array.from(this.nodes.values());
  }

  public getNodes(): GraphNode[] {
    return Array.from(this.nodes.values());
  }

  public getEdges(): GraphEdge[] {
    return [...this.edges];
  }

  public getClusterColor(node: GraphNode): string {
    if (node.riskScore >= 75) return '#ef4444'; // Red (High risk)
    if (node.riskScore >= 40) return '#f59e0b'; // Amber (Medium risk)
    return '#10b981'; // Green (Authentic)
  }
}
