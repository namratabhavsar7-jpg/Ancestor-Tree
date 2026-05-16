/**
 * CORE TREE LOGIC (BFS BASED)
 * Based on user-provided algorithm for fixed grid positioning.
 */

const TreeLogic = {
    // 1. Transform flat data (nodes/links) into the hierarchy format
    buildFamilyObject: function(nodes, links) {
        const family = {};
        nodes.forEach(n => {
            family[n.id] = { ...n, children: [] };
        });
        links.forEach(l => {
            if (l.type === 'parent') {
                if (family[l.source]) {
                    family[l.source].children.push(l.target);
                }
            }
        });
        return family;
    },

    // 2. BFS Hierarchy Generation
    bfsHierarchy: function(family, rootId) {
        const generations = {};
        const queue = [{ id: rootId, gen: 0 }];
        const visited = new Set();

        while (queue.length) {
            const current = queue.shift();
            if (visited.has(current.id)) continue;
            visited.add(current.id);

            generations[current.id] = current.gen;

            if (family[current.id] && family[current.id].children) {
                family[current.id].children.forEach(childId => {
                    queue.push({ id: childId, gen: current.gen + 1 });
                });
            }
        }
        return generations;
    },

    // 3. Grouping by Generation
    groupByGeneration: function(generations) {
        const groups = {};
        Object.entries(generations).forEach(([id, gen]) => {
            if (!groups[gen]) groups[gen] = [];
            groups[gen].push(Number(id));
        });
        return groups;
    },

    // 4. Position Calculation (Fixed Grid)
    calculatePositions: function(groups) {
        const positions = {};
        Object.entries(groups).forEach(([gen, nodes]) => {
            nodes.forEach((id, index) => {
                positions[id] = {
                    x: 150 + (index * 240), // Increased spacing slightly for better card fit
                    y: 100 + (gen * 200)
                };
            });
        });
        return positions;
    },

    // Master function to get everything ready
    generateTreeLayout: function(nodes, links) {
        const family = this.buildFamilyObject(nodes, links);
        
        // Find roots (nodes that aren't children in 'parent' links)
        const childIds = new Set(links.filter(l => l.type === 'parent').map(l => l.target));
        const roots = nodes.filter(n => !childIds.has(n.id));
        
        if (!roots.length && nodes.length) roots.push(nodes[0]);

        const allPositions = {};
        const allGenerations = {};

        roots.forEach(root => {
            const generations = this.bfsHierarchy(family, root.id);
            const groups = this.groupByGeneration(generations);
            const positions = this.calculatePositions(groups);
            
            Object.assign(allPositions, positions);
            Object.assign(allGenerations, generations);
        });

        return { family, positions: allPositions, generations: allGenerations };
    }
};
